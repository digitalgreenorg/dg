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

    var DigitalGreenPageController = require('controllers/DigitalGreenPageController');
    var CollectionFiltersViewController = require('app/view-controllers/CollectionFiltersViewController');
    var CollectionMostFiltersViewController = require('app/view-controllers/CollectionMostFiltersViewController');
    var CollectionViewController = require('app/view-controllers/CollectionViewController');
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
            references.collectionMostFiltersViewController.setActiveFilter('-_score');
            return this;
        },

        _initReferences: function() {
            this.base();

            var references = this._references;

            var $collectionsContainer = jQuery('.js-collections-wrapper');
            var $filtersWrapper = jQuery('.js-filters-wrapper');

            // helpers
            var $languageCookie = -1
            references.collectionFiltersViewController = new CollectionFiltersViewController($filtersWrapper);
            references.collectionViewController = new CollectionViewController($collectionsContainer, $languageCookie);
            references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);
        },

        _initEvents: function() {
            this.base();

            var references = this._references;
            var boundFunctions = this._boundFunctions;
            
         // filters changed
            boundFunctions.onFilterChanged = this._onFilterChanged.bind(this);
            references.collectionFiltersViewController.on('filterChanged', boundFunctions.onFilterChanged);

            // collections updated
            boundFunctions.onCollectionDataProcessed = this._onCollectionDataProcessed.bind(this);
            references.collectionViewController.on('collectionsUpdated', boundFunctions.onCollectionDataProcessed);

            // order changed
            boundFunctions.onOrderChanged = this._onOrderChanged.bind(this);
            references.collectionMostFiltersViewController.on('orderChanged', boundFunctions.onOrderChanged);

            // filters cleared
            boundFunctions.onFiltersCleared = this._onFiltersCleared.bind(this);
            references.collectionFiltersViewController.on('filtersCleared', boundFunctions.onFiltersCleared);
        },

        _onCollectionDataProcessed: function(broadcastData) {
            var set_filters = this._references.collectionFiltersViewController._references.dataFeed;
            var filter_object = this._references.collectionViewController._references.dataFeed._state.inputParams.filters.value;
            var facets = this._references.collectionViewController._references.dataFeed._dataModel._data.facets;
            if (filter_object){
                set_filters.addInputParam('filters', true, 0, true);
                set_filters.setInputParam('filters', filter_object, true);
            }
            set_filters.addInputParam('facets', true, 0, true);
            set_filters.setInputParam('facets', facets, true);
            this._references.collectionFiltersViewController._fetchFilters("POST");
            this._references.collectionFiltersViewController.updateTotalCount(broadcastData.totalCount);
            // Only if data attributes are to be used, go inside this loop
            if (this._references.collectionFiltersViewController._references.filters_cleared == 0){
                if ($(".js-collections-wrapper").attr('data-partner') != 'None' ){
                    this._references.collectionFiltersViewController._setFilterStatus('partner', $(".js-collections-wrapper").attr('data-partner'), true);
                }
                if ($(".js-collections-wrapper").attr('data-title') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('topic', $(".js-collections-wrapper").attr('data-title'), true);
                    this._references.collectionFiltersViewController._setFilterStatus('subject', $(".js-collections-wrapper").attr('data-title'), true);
                }
                if ($(".js-collections-wrapper").attr('data-state') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('state', $(".js-collections-wrapper").attr('data-state'), true);
                }
                if ($(".js-collections-wrapper").attr('data-language') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('language', $(".js-collections-wrapper").attr('data-language'), true);
                }
                if ($(".js-collections-wrapper").attr('data-category') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('category', $(".js-collections-wrapper").attr('data-category'), true);
                }
                if ($(".js-collections-wrapper").attr('data-subcategory') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('subcategory', $(".js-collections-wrapper").attr('data-subcategory'), true);
                }
                if ($(".js-collections-wrapper").attr('data-topic') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('topic', $(".js-collections-wrapper").attr('data-topic'), true);
                }
                if ($(".js-collections-wrapper").attr('data-subject') != 'None'){
                    this._references.collectionFiltersViewController._setFilterStatus('subject', $(".js-collections-wrapper").attr('data-subject'), true);
                }
            }
        },

        _onOrderChanged: function(orderCriteria) {
            this._references.collectionViewController.setInputParam('order_by', orderCriteria);
        },

        _onFilterChanged: function(filterParam, filterValue, active) {
            this._references.collectionViewController.setFilterStatus(filterParam, filterValue, active);
        },

        _onFiltersCleared: function() {
            this._references.collectionFiltersViewController._references.filters_cleared = 1; // remove usage of data-attributes
            this._references.collectionViewController._references.dataFeed.setInputParam('filters',0,true);
            this._references.collectionFiltersViewController._references.dataFeed.setInputParam('filters',0,true);
            this._references.collectionViewController._references.dataFeed.setInputParam('searchString','None');
            this._references.collectionViewController._references.dataFeed._fetch();
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
