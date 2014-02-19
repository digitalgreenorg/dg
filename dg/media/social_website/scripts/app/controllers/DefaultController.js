/**
 * DefaultController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var jQuery = require('jquery');

    var DefaultController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {AboutController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);
            return this;
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return DefaultController;
});
