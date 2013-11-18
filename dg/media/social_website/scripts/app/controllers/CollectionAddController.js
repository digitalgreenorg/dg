/**
 * CollectionAddController Class File
 *
 * @author Aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var CollectionDropDownController = require('app/view-controllers/CollectionDropDownController')
    var jQuery = require('jquery');
    var sortable = require('libs/external/jquery-ui');

    var CollectionAddController = DigitalGreenPageController.extend({

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
            var $collectionWrapper = jQuery('.js-collection-outer-wrapper');
            $( "#sortable" ).sortable({
            	                delay: 100,
            	                revert: 300
            	            });
            $( "#sortable" ).disableSelection();
            
            //var $filtersWrapper = jQuery('.js-filters-wrapper');

            // helpers
            var $languageCookie = -1
            references.CollectionDropDownController = new CollectionDropDownController($collectionWrapper);
            references.$saveButton = jQuery('.collection-save-button');
            //references.collectionViewController = new CollectionViewController($collectionsContainer, $languageCookie);
            //references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);
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

    return CollectionAddController;
});
