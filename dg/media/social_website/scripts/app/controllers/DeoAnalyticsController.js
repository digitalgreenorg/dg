/**
 * DeoAnalyticsController Class File
 *
 * @author Aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('controllers/DigitalGreenPageController');
    var DeoAnalyticsViewController = require('app/view-controllers/DeoAnalyticsViewController')
    var jQuery = require('jquery');

    var DeoAnalyticsController = DigitalGreenPageController.extend({

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
            references.DeoAnalyticsViewController = new DeoAnalyticsViewController($analyticsWrapper);
            
            var today = new Date();
            references.DeoAnalyticsViewController.setDate(0, today);
            references.DeoAnalyticsViewController.setWeekSingleDate(new Date());
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

    return DeoAnalyticsController;
});
