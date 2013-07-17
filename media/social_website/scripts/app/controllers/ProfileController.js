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
            var currentPage = 0;
            var collectionsPerPage = 4;

            references.collectionViewController
                .setCollectionsPerPage(4)
                .setCollectionsPerRow(4)
                .setVideosPerDrawer(5);

            // set the active filter to be Most Liked to init the collections
            references.collectionMostFiltersViewController.setActiveFilter('-likes');
            var partner_uid = $(".js-partner-farmers-pages-container").attr('data-partnerID') ;
            this._references.collectionViewController._references.dataFeed.addInputParam('uid', true, 0, true);
            this._references.collectionViewController._references.dataFeed.setInputParam('uid', partner_uid, true);
            this._getCollections(0,4);

            return this;
        },

        _initReferences: function($referenceBase, params) {
            this.base($referenceBase);

            var references = this._references;
  
            var $collectionsContainer = jQuery('.js-collections-wrapper');
            references.collectionViewController = new CollectionViewController($collectionsContainer);
            references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);

            // TODO var $activitiesContainer = jQuery('.js-activities-container');
            // TODO references.activitiesViewController = new ActivitiesViewController($activitiesContainer);
            
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
            
            // show more
            boundFunctions.onShowMoreClick = this._onShowMoreClick.bind(this);
            references.$showMoreButton.on('click', boundFunctions.onShowMoreClick);

            boundFunctions.onHideCollectionsClick = this._onHideCollectionsClick.bind(this);
            references.$hideCollectionsButton.on('click', boundFunctions.onHideCollectionsClick);
        },
        
        
        _onOrderChanged: function(orderCriteria) {
            this._references.collectionViewController.setInputParam('order_by', orderCriteria);
        },

        _getCollections: function(page,count) {
            return this._references.collectionViewController.getCollections(page,count);
        },
        
        _onShowMoreClick: function(e) {
            e.preventDefault();
            this._references.collectionViewController._references.dataFeed.setInputParam('offset', 4, true);
            var collectionData = this._getCollections(1,4);
            this._renderPartialCollections
            
            //this._getCollectionsPage('next');
        },
        
        _onHideCollectionsClick: function(e) {
            e.preventDefault();

            var references = this._references;

            var $collectionsPages = references.$collectionsContainer.find('.js-collections-page');

            if ($collectionsPages.length <= 1) {
                return;
            }

            var $pageToRemove = $collectionsPages.eq($collectionsPages.length - 1);
            var updateHideCollectionsButtonDisplayBind = this._updateHideCollectionsButtonDisplay.bind(this);
            $pageToRemove
                .animate({
                    height: '0px'
                }, function() {
                    $pageToRemove.remove();
                    updateHideCollectionsButtonDisplayBind();
                });

            this._setCollectionsPage('previous');

            references.$showMoreButton.show();
        },
        
        _renderPartialCollections: function(collectionHTML) {
            var $div = jQuery('<div />');
            $div.append(collectionHTML);
            var $page = $div.find('.js-collections-page');
            $page.css({
                position: 'absolute',
                visibility: 'hidden'
            });

            this._references.$collectionsContainer.append($page);

            var height = $page.height();
            $page.css({
                height: '0px',
                position: '',
                visibility: ''
            });

            $page.animate({
                height: height + 'px'
            }, function() {
                $page.css({
                    height: ''
                });
            });
            
            //this._updateHideCollectionsButtonDisplay();
            //this._initVideoCarousels();
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
