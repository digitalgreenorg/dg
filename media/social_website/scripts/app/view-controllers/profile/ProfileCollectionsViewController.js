/**
 * RecentlyViewedCollectionsViewController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var GenericCollectionsViewController = require('app/view-controllers/GenericCollectionsViewController');
    var NCarousel = require('libs/NCarousel/NCarousel');

    var GenericCollectionsDataFeed = require('app/libs/GenericCollectionsDataFeed');

    var collectionTemplate = require('text!app/views/collection.html');
    var collectionVideoDrawerTemplate = require('text!app/views/collection-video-drawer.html');


    var RecentlyViewedCollectionsViewController = GenericCollectionsViewController.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase, params) {

            // set up params prior to calling parent
            if (params == undefined) {
                params = {};
            }

            // call parent
            this.base($referenceBase, params);
            
            this._setActiveCollection('recent');
            this._getCollectionsPage('first');

            return this;
        },

        _initReferences: function($referenceBase, params) {
            this.base($referenceBase, params);

            var references = this._references;
            
            // data feeds
            
            //change back to
            // var recentlyViewedDataFeed = new GenericCollectionsDataFeed('api/recentlyViewed');
            // after user is added and recently viewed is recorded
            var recentlyViewedDataFeed = new GenericCollectionsDataFeed('api/collectionsSearch');
            //
            recentlyViewedDataFeed.addInputParam('userId', true);
            this._addCollectionsDataFeed('recent', recentlyViewedDataFeed);

            //change back to
            // var recentlyViewedDataFeed = new GenericCollectionsDataFeed('api/recentlyViewed');
            // after user is added and recently viewed is recorded
            var completedCollectionsDataFeed = new GenericCollectionsDataFeed('api/collectionsSearch');
            //
            completedCollectionsDataFeed.addInputParam('userId', true);
            this._addCollectionsDataFeed('completed', completedCollectionsDataFeed);

            // html element references
            references.$profileWrapper = $referenceBase;
            references.$showMoreButton = $referenceBase.find('.js-show-more');
            references.$hideCollectionsButton = $referenceBase.find('.js-hide-collections');
            references.$collectionsContainer = $referenceBase.find('.js-collections-container');
        },

        _initEvents: function(params) {
            this.base();

            var references = this._references;
            var boundFunctions = this._boundFunctions;

            // collection type switching buttons (Recent, Completed)
            boundFunctions.onCollectionTypeClick = this._onCollectionDisplayTypeClick.bind(this);
            references.$profileWrapper.on('click', '.js-collection-type', boundFunctions.onCollectionTypeClick);

            // show more
            boundFunctions.onShowMoreClick = this._onShowMoreClick.bind(this);
            references.$showMoreButton.on('click', boundFunctions.onShowMoreClick);

            boundFunctions.onHideCollectionsClick = this._onHideCollectionsClick.bind(this);
            references.$hideCollectionsButton.on('click', boundFunctions.onHideCollectionsClick);
        },

        _initState: function(params) {
            this.base();

            var state = this._state;
            state.currentPage = 0;

            var collectionsPerPage = 4;

            this
                .setCollectionsPerRow(4)
                .setCollectionsPerPage(collectionsPerPage)
                .setVideoDrawerClasses('')
                .setVideosPerDrawer(5);

            // TODO: where do we get the uid from??
            this
                ._setAllCollectionsInputParam('offset', state.currentPage)
                ._setAllCollectionsInputParam('limit', collectionsPerPage)
                ._setAllCollectionsInputParam('userId', 1337);
        },

        _onCollectionDisplayTypeClick: function(e) {
            e.preventDefault();

            var $currentTarget = jQuery(e.currentTarget);
            var newCollectionId = $currentTarget.data('collection-id');

            this._setActiveCollection(newCollectionId);

            var currentCollectionsData = this._getAllCurrentCollectionsPages();

            // on first load of each collection, we won't have any data
            // therefore, we'll ensure we have some data to display
            if (currentCollectionsData.collections.length == 0) {
                this._getCollectionsPage('first');
            }
        },

        _onShowMoreClick: function(e) {
            e.preventDefault();
            this._getCollectionsPage('next');
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

        _onTotalNumberOfCollectionsReached: function(collectionId, feedInformation) {
            this.base();

            if (feedInformation.currentPage >= feedInformation.totalPages - 1) {
                this._references.$showMoreButton.hide();
            }

        },

        _setActiveCollection: function(newCollectionId) {
            var $collectionOptions = this._references.$profileWrapper.find('.js-collection-type');

            // get the previously active filter id
            var oldCollectionId = $collectionOptions.filter('.active').data('collection-id');

            // exit early if the filter hasn't changed
            // TODO: might we want the filter changing to be a toggle on/off?
            if (newCollectionId == oldCollectionId) {
                return;
            }

            // get new filter element
            var $newFilterElement = $collectionOptions.filter('[data-collection-id=' + newCollectionId + ']');

            // clear active classes
            $collectionOptions.removeClass('active');
            // add new active class
            $newFilterElement.addClass('active');

            // reveal the show more button again
            this._references.$showMoreButton.show();

            this._setCurrentCollectionsDataFeed(newCollectionId);
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
            
            this._updateHideCollectionsButtonDisplay();
            this._initVideoCarousels();
        },

        _renderAllCollections: function(collectionHTML) {
            this._references.$collectionsContainer.html(collectionHTML);
            this._updateHideCollectionsButtonDisplay();
            this._initVideoCarousels();
        },

        _updateHideCollectionsButtonDisplay: function() {
            var references = this._references;

            var $collectionsPages = references.$collectionsContainer.find('.js-collections-page');

            if ($collectionsPages.length <= 1) {
                references.$hideCollectionsButton.hide();
            } else {
                references.$hideCollectionsButton.show();
            }
        },

        _initVideoCarousels: function() {
            var $carouselWrappers = this._references.$collectionsContainer.find('.js-carousel-wrapper');

            var i = 0;
            var len = $carouselWrappers.length;
            for (; i < len; i++) {
                var $currentCarouselWrapper = $carouselWrappers.eq(i);
                new NCarousel($currentCarouselWrapper, {
                    transition: 'basic',
                    autoPlay: false,
                    allowWrapping: false
                });
            }
        },


        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();

            // TODO: clean up
        }
    });

    return RecentlyViewedCollectionsViewController;
});
