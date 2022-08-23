swiss.define('web.ajax_external', function (require) {
"use strict";

var ajax = require('web.ajax');

/**
  * This file should be used in the context of an external widget loading (e.g: live chat in a non-SwissCRM website)
  * It overrides the 'loadJS' method that is supposed to load additional scripts, based on a relative URL (e.g: '/web/webclient/locale/en_US')
  * As we're not in an SwissCRM website context, the calls will not work, and we avoid a 404 request.
  */
ajax.loadJS = function (url) {
    console.warn('Tried to load the following script on an external website: ' + url);
};
});
