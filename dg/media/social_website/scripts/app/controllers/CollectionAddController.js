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
    var CollectionAddViewController = require('app/view-controllers/CollectionAddViewController')
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
            var $sortable = jQuery('#sortable');
            
            // Initializing Sortable for Dragging around videos
            
            $( $sortable ).sortable({
            	                delay: 100,
            	                scroll: false,
            	                cursorAt: { top:0, left: 0 },
            	            });
            $( $sortable ).disableSelection();
            
            
            references.CollectionAddViewController = new CollectionAddViewController($collectionWrapper);
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
