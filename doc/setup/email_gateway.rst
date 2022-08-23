:banner: banners/email_gateway.jpg

=====================
SwissCRM email gateway
=====================

The SwissCRM mail gateway allows you to inject directly all the received emails in SwissCRM.

Its principle is straightforward: your SMTP server executes the "mailgate" script for every new incoming email.

The script takes care of connecting to your SwissCRM database through XML-RPC, and send the emails via
the `MailThread.message_process()` feature.

Prerequisites
-------------
- Administrator access to the SwissCRM database.
- Your own mail server such as Postfix or Exim.
- Technical knowledge on how to configure an email server.

For Postfix
-----------
In you alias config (:file:`/etc/aliases`):

.. code-block:: text

   email@address: "|/swiss-directory/addons/mail/static/scripts/swiss-mailgate.py -d <database-name> -u <userid> -p <password>"

.. note::
   Resources

   - `Postfix <http://www.postfix.org/documentation.html>`_
   - `Postfix aliases <http://www.postfix.org/aliases.5.html>`_
   - `Postfix virtual <http://www.postfix.org/virtual.8.html>`_


For Exim
--------
.. code-block:: text

   *: |/swiss-directory/addons/mail/static/scripts/swiss-mailgate.py -d <database-name> -u <userid> -p <password>

.. note::
   Resources

   - `Exim <https://www.exim.org/docs.html>`_

.. tip::
   If you don't have access/manage your email server, use `inbound messages
   <https://www.swissconsultings.ch/documentation/user/14.0/discuss/advanced/email_servers.html#how-to-manage-outbound-messages>`_.
