swiss.define('iap.redirect_swiss_credit_widget', function(require) {
"use strict";

var AbstractAction = require('web.AbstractAction');
var core = require('web.core');


var IapSwissCRMCreditRedirect = AbstractAction.extend({
    template: 'iap.redirect_to_swiss_credit',
    events : {
        "click .redirect_confirm" : "swiss_redirect",
    },
    init: function (parent, action) {
        this._super(parent, action);
        this.url = action.params.url;
    },

    swiss_redirect: function () {
        window.open(this.url, '_blank');
        this.do_action({type: 'ir.actions.act_window_close'});
        // framework.redirect(this.url);
    },

});
core.action_registry.add('iap_swiss_credit_redirect', IapSwissCRMCreditRedirect);
});
