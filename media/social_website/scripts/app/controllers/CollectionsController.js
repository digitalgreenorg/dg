/**
 * CollectionsController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var CollectionViewController = require('app/view-controllers/CollectionViewController');
    var CollectionMostFiltersViewController = require('app/view-controllers/CollectionMostFiltersViewController');
    var CollectionFiltersViewController = require('app/view-controllers/CollectionFiltersViewController');
    var jQuery = require('jquery');

    var CollectionsController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {CollectionsController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            var references = this._references;

            references.collectionViewController
                .setCollectionsPerPage(12)
                .setCollectionsPerRow(3)
                .setVideoDrawerClasses('vidDrawer-wrapper-short vidDrawer-alt-bg')
                .setVideosPerDrawer(4);

            // set the active filter to be Most Liked to init the collections
            references.collectionMostFiltersViewController.setActiveFilter('-likes');

            return this;
        },

        _initReferences: function() {
            this.base();

            var references = this._references;

            var $collectionsContainer = jQuery('.js-collections-wrapper');
            var $filtersWrapper = jQuery('.js-filters-wrapper');

            // helpers
            references.collectionViewController = new CollectionViewController($collectionsContainer);
            references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);
            references.collectionFiltersViewController = new CollectionFiltersViewController($filtersWrapper);
        },

        _initEvents: function() {
            this.base();

            var references = this._references;
            var boundFunctions = this._boundFunctions;

            // collections updated
            boundFunctions.onCollectionDataProcessed = this._onCollectionDataProcessed.bind(this);
            references.collectionViewController.on('collectionsUpdated', boundFunctions.onCollectionDataProcessed);

            // order changed
            boundFunctions.onOrderChanged = this._onOrderChanged.bind(this);
            references.collectionMostFiltersViewController.on('orderChanged', boundFunctions.onOrderChanged);

            // filters changed
            boundFunctions.onFilterChanged = this._onFilterChanged.bind(this);
            references.collectionFiltersViewController.on('filterChanged', boundFunctions.onFilterChanged);

            // filters cleared
            boundFunctions.onFiltersCleared = this._onFiltersCleared.bind(this);
            references.collectionFiltersViewController.on('filtersCleared', boundFunctions.onFiltersCleared);
        },

        _onCollectionDataProcessed: function(broadcastData) {
            this._references.collectionFiltersViewController.updateTotalCount(broadcastData.totalCount);
        },

        _onOrderChanged: function(orderCriteria) {
            this._references.collectionViewController.setInputParam('order_by', orderCriteria);
        },

        _onFilterChanged: function(filterParam, filterValue, active) {
            this._references.collectionViewController.setFilterStatus(filterParam, filterValue, active);
        },

        _onFiltersCleared: function() {
            this._references.collectionViewController.clearFilters();
        },

        _getCollections: function() {
            this._references.collectionViewController.getCollections();
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return CollectionsController;
});
