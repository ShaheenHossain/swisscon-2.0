# -*- coding: utf-8 -*-
# Part of Odoo, SwissCRM. See LICENSE file for full copyright and licensing details.

import base64

from unittest.mock import patch

from swiss.addons.test_mail.data.test_mail_data import MAIL_TEMPLATE_PLAINTEXT
from swiss.addons.test_mail.models.test_mail_models import MailTestSimple
from swiss.addons.test_mail.tests.common import TestMailCommon, TestRecipients
from swiss.api import call_kw
from swiss.exceptions import AccessError
from swiss.tests import tagged
from swiss.tools import mute_logger, formataddr
from swiss.tests.common import users


@tagged('mail_post')
class TestMessagePost(TestMailCommon, TestRecipients):

    @classmethod
    def setUpClass(cls):
        super(TestMessagePost, cls).setUpClass()
        cls._create_portal_user()
        cls.test_record = cls.env['mail.test.simple'].with_context(cls._test_context).create({'name': 'Test', 'email_from': 'ignasse@example.com'})
        cls._reset_mail_context(cls.test_record)
        cls.user_admin.write({'notification_type': 'email'})

    # This method should be run inside a post_install class to ensure that all
    # message_post overrides are tested.
    def test_message_post_return(self):
        test_channel = self.env['mail.channel'].create({
            'name': 'Test',
        })
        # Use call_kw as shortcut to simulate a RPC call.
        messageId = call_kw(self.env['mail.channel'], 'message_post', [test_channel.id], {'body': 'test'})
        self.assertTrue(isinstance(messageId, int))

    @users('employee')
    def test_notify_mail_add_signature(self):
        self.test_track = self.env['mail.test.track'].with_context(self._test_context).with_user(self.user_employee).create({
            'name': 'Test',
            'email_from': 'ignasse@example.com'
        })
        self.test_track.user_id = self.env.user

        signature = self.env.user.signature

        template = self.env.ref('mail.mail_notification_paynow', raise_if_not_found=True).sudo()
        self.assertIn("record.user_id.sudo().signature", template.arch)

        with self.mock_mail_gateway():
            self.test_track.message_post(body="Test body", mail_auto_delete=False, add_sign=True, partner_ids=[self.partner_1.id, self.partner_2.id], email_layout_xmlid="mail.mail_notification_paynow")
        found_mail = self._new_mails
        self.assertIn(signature, found_mail.body_html)
        self.assertEqual(found_mail.body_html.count(signature), 1)

        with self.mock_mail_gateway():
            self.test_track.message_post(body="Test body", mail_auto_delete=False, add_sign=False, partner_ids=[self.partner_1.id, self.partner_2.id], email_layout_xmlid="mail.mail_notification_paynow")
        found_mail = self._new_mails
        self.assertNotIn(signature, found_mail.body_html)
        self.assertEqual(found_mail.body_html.count(signature), 0)

    @users('employee')
    def test_notify_prepare_template_context_company_value(self):
        """ Verify that the template context company value is right
        after switching the env company or if a company_id is set
        on mail record.
        """
        current_user = self.env.user
        main_company = current_user.company_id
        other_company = self.env['res.company'].with_user(self.user_admin).create({'name': 'Company B'})
        current_user.sudo().write({'company_ids': [(4, other_company.id)]})
        test_record = self.env['mail.test.multi.company'].with_user(self.user_admin).create({
            'name': 'Multi Company Record',
            'company_id': False,
        })

        # self.env.company.id = Main Company    AND    test_record.company_id = False
        self.assertEqual(self.env.company.id, main_company.id)
        self.assertEqual(test_record.company_id.id, False)
        template_values = test_record._notify_prepare_template_context(test_record.message_ids, {})
        self.assertEqual(template_values.get('company').id, self.env.company.id)

        # self.env.company.id = Other Company    AND    test_record.company_id = False
        current_user.company_id = other_company
        test_record = self.env['mail.test.multi.company'].browse(test_record.id)
        self.assertEqual(self.env.company.id, other_company.id)
        self.assertEqual(test_record.company_id.id, False)
        template_values = test_record._notify_prepare_template_context(test_record.message_ids, {})
        self.assertEqual(template_values.get('company').id, self.env.company.id)

        # self.env.company.id = Other Company    AND    test_record.company_id = Main Company
        test_record.company_id = main_company
        test_record = self.env['mail.test.multi.company'].browse(test_record.id)
        self.assertEqual(self.env.company.id, other_company.id)
        self.assertEqual(test_record.company_id.id, main_company.id)
        template_values = test_record._notify_prepare_template_context(test_record.message_ids, {})
        self.assertEqual(template_values.get('company').id, main_company.id)

    def test_notify_recipients_internals(self):
        pdata = self._generate_notify_recipients(self.partner_1 | self.partner_employee)
        msg_vals = {
            'body': 'Message body',
            'model': self.test_record._name,
            'res_id': self.test_record.id,
            'subject': 'Message subject',
        }
        link_vals = {
            'token': 'token_val',
            'access_token': 'access_token_val',
            'auth_signup_token': 'auth_signup_token_val',
            'auth_login': 'auth_login_val',
        }
        notify_msg_vals = dict(msg_vals, **link_vals)
        classify_res = self.env[self.test_record._name]._notify_classify_recipients(pdata, 'My Custom Model Name', msg_vals=notify_msg_vals)
        # find back information for each recipients
        partner_info = next(item for item in classify_res if item['recipients'] == self.partner_1.ids)
        emp_info = next(item for item in classify_res if item['recipients'] == self.partner_employee.ids)

        # partner: no access button
        self.assertFalse(partner_info['has_button_access'])

        # employee: access button and link
        self.assertTrue(emp_info['has_button_access'])
        for param, value in link_vals.items():
            self.assertIn('%s=%s' % (param, value), emp_info['button_access']['url'])
        self.assertIn('model=%s' % self.test_record._name, emp_info['button_access']['url'])
        self.assertIn('res_id=%s' % self.test_record.id, emp_info['button_access']['url'])
        self.assertNotIn('body', emp_info['button_access']['url'])
        self.assertNotIn('subject', emp_info['button_access']['url'])

        # test when notifying on non-records (e.g. MailThread._message_notify())
        for model, res_id in ((self.test_record._name, False),
                              (self.test_record._name, 0),  # browse(0) does not return a valid recordset
                              (False, self.test_record.id),
                              (False, False),
                              ('mail.thread', False),
                              ('mail.thread', self.test_record.id)):
            msg_vals.update({
                'model': model,
                'res_id': res_id,
            })
            # note that msg_vals wins over record on which method is called
            notify_msg_vals = dict(msg_vals, **link_vals)
            classify_res = self.test_record._notify_classify_recipients(
                pdata, 'Test', msg_vals=notify_msg_vals)
            # find back information for partner
            partner_info = next(item for item in classify_res if item['recipients'] == self.partner_1.ids)
            emp_info = next(item for item in classify_res if item['recipients'] == self.partner_employee.ids)
            # check there is no access button
            self.assertFalse(partner_info['has_button_access'])
            self.assertFalse(emp_info['has_button_access'])

            # test on falsy records (False model cannot be browsed, skipped)
            if model:
                record_falsy = self.env[model].browse(res_id)
                classify_res = record_falsy._notify_classify_recipients(
                    pdata, 'Test', msg_vals=notify_msg_vals)
                # find back information for partner
                partner_info = next(item for item in classify_res if item['recipients'] == self.partner_1.ids)
                emp_info = next(item for item in classify_res if item['recipients'] == self.partner_employee.ids)
                # check there is no access button
                self.assertFalse(partner_info['has_button_access'])
                self.assertFalse(emp_info['has_button_access'])

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_needaction(self):
        (self.user_employee | self.user_admin).write({'notification_type': 'inbox'})
        with self.assertSinglePostNotifications([{'partner': self.partner_employee, 'type': 'inbox'}], {'content': 'Body'}):
            self.test_record.message_post(
                body='Body', message_type='comment', subtype_xmlid='mail.mt_comment',
                partner_ids=[self.user_employee.partner_id.id])

        self.test_record.message_subscribe([self.partner_1.id])
        with self.assertSinglePostNotifications([
                {'partner': self.partner_employee, 'type': 'inbox'},
                {'partner': self.partner_1, 'type': 'email'}], {'content': 'NewBody'}):
            self.test_record.message_post(
                body='NewBody', message_type='comment', subtype_xmlid='mail.mt_comment',
                partner_ids=[self.user_employee.partner_id.id])

        with self.assertSinglePostNotifications([
                {'partner': self.partner_1, 'type': 'email'},
                {'partner': self.partner_portal, 'type': 'email'}], {'content': 'ToPortal'}):
            self.test_record.message_post(
                body='ToPortal', message_type='comment', subtype_xmlid='mail.mt_comment',
                partner_ids=[self.partner_portal.id])

    def test_post_inactive_follower(self):
        # In some case swissbot is follower of a record.
        # Even if it shouldn't be the case, we want to be sure that swissbot is not notified
        (self.user_employee | self.user_admin).write({'notification_type': 'inbox'})
        self.test_record._message_subscribe(self.user_employee.partner_id.ids)
        with self.assertSinglePostNotifications([{'partner': self.partner_employee, 'type': 'inbox'}], {'content': 'Test'}):
            self.test_record.message_post(
                body='Test', message_type='comment', subtype_xmlid='mail.mt_comment')

        self.user_employee.active = False
        # at this point, partner is still active and would receive an email notification
        self.user_employee.partner_id._write({'active': False})
        with self.assertPostNotifications([{'content': 'Test', 'notif': []}]):
            self.test_record.message_post(
                body='Test', message_type='comment', subtype_xmlid='mail.mt_comment')

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_notifications(self):
        _body, _subject = '<p>Test Body</p>', 'Test Subject'

        # subscribe second employee to the group to test notifications
        self.test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id])

        with self.assertSinglePostNotifications(
                [{'partner': self.partner_1, 'type': 'email'},
                 {'partner': self.partner_2, 'type': 'email'},
                 {'partner': self.partner_admin, 'type': 'email'}],
                {'content': _body},
                mail_unlink_sent=True):
            msg = self.test_record.with_user(self.user_employee).message_post(
                body=_body, subject=_subject,
                message_type='comment', subtype_xmlid='mail.mt_comment',
                partner_ids=[self.partner_1.id, self.partner_2.id]
            )

        # message content
        self.assertEqual(msg.subject, _subject)
        self.assertEqual(msg.body, _body)
        self.assertEqual(msg.partner_ids, self.partner_1 | self.partner_2)
        self.assertEqual(msg.notified_partner_ids, self.user_admin.partner_id | self.partner_1 | self.partner_2)
        self.assertEqual(msg.channel_ids, self.env['mail.channel'])

        # notifications emails should have been deleted
        self.assertFalse(self.env['mail.mail'].sudo().search([('mail_message_id', '=', msg.id)]),
                         'message_post: mail.mail notifications should have been auto-deleted')

    @mute_logger('swiss.addons.mail.models.mail_mail', 'swiss.tests')
    def test_post_notifications_keep_emails(self):
        self.test_record.message_subscribe(partner_ids=[self.user_admin.partner_id.id])

        msg = self.test_record.with_user(self.user_employee).message_post(
            body='Test', subject='Test',
            message_type='comment', subtype_xmlid='mail.mt_comment',
            partner_ids=[self.partner_1.id, self.partner_2.id],
            mail_auto_delete=False
        )

        # notifications emails should not have been deleted: one for customers, one for user
        self.assertEqual(len(self.env['mail.mail'].sudo().search([('mail_message_id', '=', msg.id)])), 2)

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_notifications_emails_tweak(self):
        pass
        # we should check _notification_groups behavior, for emails and buttons

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_attachments(self):
        _attachments = [
            ('List1', b'My first attachment'),
            ('List2', b'My second attachment')
        ]
        _attach_1 = self.env['ir.attachment'].with_user(self.user_employee).create({
            'name': 'Attach1',
            'datas': 'bWlncmF0aW9uIHRlc3Q=',
            'res_model': 'mail.compose.message', 'res_id': 0})
        _attach_2 = self.env['ir.attachment'].with_user(self.user_employee).create({
            'name': 'Attach2',
            'datas': 'bWlncmF0aW9uIHRlc3Q=',
            'res_model': 'mail.compose.message', 'res_id': 0})

        with self.mock_mail_gateway():
            msg = self.test_record.with_user(self.user_employee).message_post(
                body='Test', subject='Test',
                message_type='comment', subtype_xmlid='mail.mt_comment',
                attachment_ids=[_attach_1.id, _attach_2.id],
                partner_ids=[self.partner_1.id],
                attachments=_attachments,
            )

        # message attachments
        self.assertEqual(len(msg.attachment_ids), 4)
        self.assertEqual(set(msg.attachment_ids.mapped('res_model')), set([self.test_record._name]))
        self.assertEqual(set(msg.attachment_ids.mapped('res_id')), set([self.test_record.id]))
        self.assertEqual(set([base64.b64decode(x) for x in msg.attachment_ids.mapped('datas')]),
                         set([b'migration test', _attachments[0][1], _attachments[1][1]]))
        self.assertTrue(set([_attach_1.id, _attach_2.id]).issubset(msg.attachment_ids.ids),
                        'message_post: mail.message attachments duplicated')

        # notification email attachments
        self.assertSentEmail(self.user_employee.partner_id, [self.partner_1])
        # self.assertEqual(len(self._mails), 1)
        self.assertEqual(len(self._mails[0]['attachments']), 4)
        self.assertIn(('List1', b'My first attachment', 'application/octet-stream'), self._mails[0]['attachments'])
        self.assertIn(('List2', b'My second attachment', 'application/octet-stream'), self._mails[0]['attachments'])
        self.assertIn(('Attach1', b'migration test', 'application/octet-stream'),  self._mails[0]['attachments'])
        self.assertIn(('Attach2', b'migration test', 'application/octet-stream'), self._mails[0]['attachments'])

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_answer(self):
        with self.mock_mail_gateway():
            parent_msg = self.test_record.with_user(self.user_employee).message_post(
                body='<p>Test</p>',
                message_type='comment',
                subject='Test Subject',
                subtype_xmlid='mail.mt_comment',
            )

        self.assertEqual(parent_msg.partner_ids, self.env['res.partner'])
        self.assertNotSentEmail()

        # post a first reply
        with self.assertPostNotifications([{'content': '<p>Test Answer</p>', 'notif': [{'partner': self.partner_1, 'type': 'email'}]}]):
            msg = self.test_record.with_user(self.user_employee).message_post(
                body='<p>Test Answer</p>',
                message_type='comment',
                subject='Welcome',
                subtype_xmlid='mail.mt_comment',
                parent_id=parent_msg.id,
                partner_ids=[self.partner_1.id],
            )

        self.assertEqual(msg.parent_id.id, parent_msg.id)
        self.assertEqual(msg.partner_ids, self.partner_1)
        self.assertEqual(parent_msg.partner_ids, self.env['res.partner'])

        # check notification emails: references
        self.assertSentEmail(
            self.user_employee.partner_id,
            [self.partner_1],
            references_content='openerp-%d-mail.test.simple' % self.test_record.id,
            # references should be sorted from the oldest to the newest
            references='%s %s' % (parent_msg.message_id, msg.message_id),
        )

        # post a reply to the reply: check parent is the first one
        with self.mock_mail_gateway():
            new_msg = self.test_record.with_user(self.user_employee).message_post(
                body='<p>Test Answer Bis</p>',
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                parent_id=msg.id,
                partner_ids=[self.partner_2.id],
            )

        self.assertEqual(new_msg.parent_id.id, parent_msg.id, 'message_post: flatten error')
        self.assertEqual(new_msg.partner_ids, self.partner_2)
        self.assertSentEmail(
            self.user_employee.partner_id,
            [self.partner_2],
            body_content='<p>Test Answer Bis</p>',
            reply_to=msg.reply_to,
            subject='Re: %s' % self.test_record.name,
            references_content='openerp-%d-mail.test.simple' % self.test_record.id,
            references='%s %s' % (parent_msg.message_id, new_msg.message_id),
        )

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_email_with_multiline_subject(self):
        _body, _body_alt, _subject = '<p>Test Body</p>', 'Test Body', '1st line\n2nd line'
        msg = self.test_record.with_user(self.user_employee).message_post(
            body=_body, subject=_subject,
            message_type='comment', subtype_xmlid='mail.mt_comment',
            partner_ids=[self.partner_1.id, self.partner_2.id]
        )
        self.assertEqual(msg.subject, '1st line 2nd line')

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_portal_ok(self):
        self.test_record.message_subscribe((self.partner_1 | self.user_employee.partner_id).ids)

        with self.assertPostNotifications([{'content': '<p>Test</p>', 'notif': [
            {'partner': self.partner_employee, 'type': 'inbox'},
            {'partner': self.partner_1, 'type': 'email'}]}
        ]), patch.object(MailTestSimple, 'check_access_rights', return_value=True):
            new_msg = self.test_record.with_user(self.user_portal).message_post(
                body='<p>Test</p>', subject='Subject',
                message_type='comment', subtype_xmlid='mail.mt_comment')

        self.assertEqual(new_msg.sudo().notified_partner_ids, (self.partner_1 | self.user_employee.partner_id))

    def test_post_portal_crash(self):
        with self.assertRaises(AccessError):
            self.test_record.with_user(self.user_portal).message_post(
                body='<p>Test</p>', subject='Subject',
                message_type='comment', subtype_xmlid='mail.mt_comment')

    @mute_logger('swiss.addons.mail.models.mail_mail', 'swiss.addons.mail.models.mail_thread')
    def test_post_internal(self):
        self.test_record.message_subscribe([self.user_admin.partner_id.id])
        msg = self.test_record.with_user(self.user_employee).message_post(
            body='My Body', subject='My Subject',
            message_type='comment', subtype_xmlid='mail.mt_note')
        self.assertEqual(msg.partner_ids, self.env['res.partner'])
        self.assertEqual(msg.notified_partner_ids, self.env['res.partner'])

        self.format_and_process(
            MAIL_TEMPLATE_PLAINTEXT, self.user_admin.email, 'not_my_businesss@example.com',
            msg_id='<1198923581.41972151344608186800.JavaMail.diff1@agrolait.com>',
            extra='In-Reply-To:\r\n\t%s\n' % msg.message_id,
            target_model='mail.test.simple')
        reply = self.test_record.message_ids - msg
        self.assertTrue(reply)
        self.assertEqual(reply.subtype_id, self.env.ref('mail.mt_note'))
        self.assertEqual(reply.notified_partner_ids, self.user_employee.partner_id)
        self.assertEqual(reply.parent_id, msg)

    def test_post_log(self):
        new_note = self.test_record.with_user(self.user_employee)._message_log(
            body='<p>Labrador</p>',
        )

        self.assertEqual(new_note.subtype_id, self.env.ref('mail.mt_note'))
        self.assertEqual(new_note.body, '<p>Labrador</p>')
        self.assertEqual(new_note.author_id, self.user_employee.partner_id)
        self.assertEqual(new_note.email_from, formataddr((self.user_employee.name, self.user_employee.email)))
        self.assertEqual(new_note.notified_partner_ids, self.env['res.partner'])

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_notify(self):
        self.user_employee.write({'notification_type': 'inbox'})

        with self.mock_mail_gateway():
            new_notification = self.test_record.message_notify(
                subject='This should be a subject',
                body='<p>You have received a notification</p>',
                partner_ids=[self.partner_1.id, self.partner_admin.id, self.user_employee.partner_id.id],
            )

        self.assertEqual(new_notification.subtype_id, self.env.ref('mail.mt_note'))
        self.assertEqual(new_notification.message_type, 'user_notification')
        self.assertEqual(new_notification.body, '<p>You have received a notification</p>')
        self.assertEqual(new_notification.author_id, self.env.user.partner_id)
        self.assertEqual(new_notification.email_from, formataddr((self.env.user.name, self.env.user.email)))
        self.assertEqual(new_notification.notified_partner_ids, self.partner_1 | self.user_employee.partner_id | self.partner_admin)
        self.assertNotIn(new_notification, self.test_record.message_ids)

        admin_mails = [x for x in self._mails if self.partner_admin.name in x.get('email_to')[0]]
        self.assertEqual(len(admin_mails), 1, 'There should be exactly one email sent to admin')
        admin_mail = admin_mails[0].get('body')
        admin_access_link = admin_mail[admin_mail.index('model='):admin_mail.index('/>') - 1] if 'model=' in admin_mail else None
  
        self.assertIsNotNone(admin_access_link, 'The email sent to admin should contain an access link')
        self.assertIn('model=%s' % self.test_record._name, admin_access_link, 'The access link should contain a valid model argument')
        self.assertIn('res_id=%d' % self.test_record.id, admin_access_link, 'The access link should contain a valid res_id argument')

        partner_mails = [x for x in self._mails if self.partner_1.name in x.get('email_to')[0]]
        self.assertEqual(len(partner_mails), 1, 'There should be exactly one email sent to partner')
        partner_mail = partner_mails[0].get('body')
        self.assertNotIn('/mail/view?model=', partner_mail, 'The email sent to admin should not contain an access link')
        # todo xdo add test message_notify on thread with followers and stuff

    @mute_logger('swiss.addons.mail.models.mail_mail')
    def test_post_post_w_template(self):
        test_record = self.env['mail.test.simple'].with_context(self._test_context).create({'name': 'Test', 'email_from': 'ignasse@example.com'})
        self.user_employee.write({
            'groups_id': [(4, self.env.ref('base.group_partner_manager').id)],
        })
        _attachments = [{
            'name': 'first.txt',
            'datas': base64.b64encode(b'My first attachment'),
            'res_model': 'res.partner',
            'res_id': self.user_admin.partner_id.id
        }, {
            'name': 'second.txt',
            'datas': base64.b64encode(b'My second attachment'),
            'res_model': 'res.partner',
            'res_id': self.user_admin.partner_id.id
        }]
        email_1 = 'test1@example.com'
        email_2 = 'test2@example.com'
        email_3 = self.partner_1.email
        self._create_template('mail.test.simple', {
            'attachment_ids': [(0, 0, _attachments[0]), (0, 0, _attachments[1])],
            'partner_to': '%s,%s' % (self.partner_2.id, self.user_admin.partner_id.id),
            'email_to': '%s, %s' % (email_1, email_2),
            'email_cc': '%s' % email_3,
        })
        # admin should receive emails
        self.user_admin.write({'notification_type': 'email'})
        # Force the attachments of the template to be in the natural order.
        self.email_template.invalidate_cache(['attachment_ids'], ids=self.email_template.ids)

        with self.mock_mail_gateway():
            test_record.with_user(self.user_employee).message_post_with_template(self.email_template.id, composition_mode='comment')

        new_partners = self.env['res.partner'].search([('email', 'in', [email_1, email_2])])
        for r in [self.partner_1, self.partner_2, new_partners[0], new_partners[1], self.partner_admin]:
            self.assertSentEmail(
                self.user_employee.partner_id,
                [r],
                subject='About %s' % test_record.name,
                body_content=test_record.name,
                attachments=[('first.txt', b'My first attachment', 'text/plain'), ('second.txt', b'My second attachment', 'text/plain')])
