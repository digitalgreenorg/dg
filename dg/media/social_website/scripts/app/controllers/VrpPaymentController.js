/**
 * Created by HP on 11/9/14.
 */
define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('controllers/DigitalGreenPageController');
    var VrpPaymentViewController = require('app/view-controllers/VrpPaymentViewController');
    var jQuery = require('jquery');
//    var dataTables = require('libs/external/jquery.dataTables.min.js');

    var VrpPaymentController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {CollectionsController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);
            var references = this._references;

            return this;
        },

        _initReferences: function() {
            this.base();
            var references = this._references;
            var $analyticsWrapper = jQuery('.js-analytics-outer-wrapper');
            references.VrpPaymentViewController = new VrpPaymentViewController($analyticsWrapper);

        },

        _initEvents: function() {
            this.base();
            var references = this._references;
            var boundFunctions = this._boundFunctions;
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return VrpPaymentController;
});
