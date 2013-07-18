/**
 * ProfileController Class File
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

    //var GenericCollectionsDataFeed = require('app/libs/GenericCollectionsDataFeed');
    //var ProfileCollectionsViewController = require('app/view-controllers/profile/ProfileCollectionsViewController');
    var CollectionMostFiltersViewController = require('app/view-controllers/CollectionMostFiltersViewController');
    var CollectionViewController = require('app/view-controllers/CollectionViewController');
    var ActivitiesViewController = require('app/view-controllers/profile/ActivitiesViewController');
    var PartnerFarmersViewController = require('app/view-controllers/PartnerFarmersViewController');
    var ProfileController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {ProfileController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);
            var references = this._references;
            var collectionsPerPage = 4;

            references.collectionViewController
                .setCollectionsPerPage(collectionsPerPage)
                .setCollectionsPerRow(4)
                .setVideosPerDrawer(5);

            // set the active filter to be Most Liked to init the collections
            references.collectionMostFiltersViewController.setActiveFilter('-likes');
            var partner_uid = $(".js-partner-farmers-pages-container").attr('data-partnerID') ;
            this._references.collectionViewController._references.dataFeed.addInputParam('uid', true, 0, true);
            this._references.collectionViewController._references.dataFeed.setInputParam('uid', partner_uid, true);
            this._getCollections(0,collectionsPerPage);

            return this;
        },

        _initReferences: function($referenceBase, params) {
            this.base($referenceBase);

            var references = this._references;
  
            var $collectionsContainer = jQuery('.js-collections-wrapper');
            references.collectionViewController = new CollectionViewController($collectionsContainer);
            references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);

            var $activitiesContainer = jQuery('.js-activities-container');
            references.activitiesViewController = new ActivitiesViewController($activitiesContainer);
            
            var $partnerFarmersCarouselContainer = jQuery(".js-partner-farmers-carousel-container");
            references.partnerFarmersViewController = new PartnerFarmersViewController($partnerFarmersCarouselContainer);
            references.$showMoreButton = jQuery(".js-show-more");
            references.$hideCollectionsButton = jQuery(".js-hide-collections");
        },
        
        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onOrderChanged = this._onOrderChanged.bind(this);
            references.collectionMostFiltersViewController.on('orderChanged', boundFunctions.onOrderChanged);
            
        },
        
        
        _onOrderChanged: function(orderCriteria) {
            this._references.collectionViewController.setInputParam('order_by', orderCriteria);
        },

        _getCollections: function(page,count) {
            return this._references.collectionViewController.getCollections(page,count);
        },
        
       
        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return ProfileController;
});
