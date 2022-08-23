swiss.define('mail_bot/static/src/models/messaging_initializer/messaging_initializer_tests.js', function (require) {
"use strict";

const { afterEach, beforeEach, start } = require('mail/static/src/utils/test_utils.js');

QUnit.module('mail_bot', {}, function () {
QUnit.module('models', {}, function () {
QUnit.module('messaging_initializer', {}, function () {
QUnit.module('messaging_initializer_tests.js', {
    beforeEach() {
        beforeEach(this);

        this.start = async params => {
            const { env, widget } = await start(Object.assign({}, params, {
                data: this.data,
            }));
            this.env = env;
            this.widget = widget;
        };
    },
    afterEach() {
        afterEach(this);
    },
});


QUnit.test('SwissCRMBot initialized at init', async function (assert) {
    // TODO this test should be completed in combination with
    // implementing _mockMailChannelInitSwissCRMBot task-2300480
    assert.expect(2);

    await this.start({
        env: {
            session: {
                swissbot_initialized: false,
            },
        },
        async mockRPC(route, args) {
            if (args.method === 'init_swissbot') {
                assert.step('init_swissbot');
            }
            return this._super(...arguments);
        },
    });

    assert.verifySteps(
        ['init_swissbot'],
        "should have initialized SwissCRMBot at init"
    );
});

});
});
});

});
