swiss.define('mail_bot/static/tests/helpers/mock_server.js', function (require) {
"use strict";

const MockServer = require('web.MockServer');

MockServer.include({
    //--------------------------------------------------------------------------
    // Private
    //--------------------------------------------------------------------------

    /**
     * @override
     */
    async _performRpc(route, args) {
        if (args.model === 'mail.channel' && args.method === 'init_swissbot') {
            return this._mockMailChannelInitSwissCRMBot();
        }
        return this._super(...arguments);
    },

    //--------------------------------------------------------------------------
    // Private Mocked Methods
    //--------------------------------------------------------------------------

    /**
     * Simulates `init_swissbot` on `mail.channel`.
     *
     * @private
     */
    _mockMailChannelInitSwissCRMBot() {
        // TODO implement this mock task-2300480
        // and improve test "SwissCRMBot initialized after 2 minutes"
    },
});

});
