/**
 * CollectionViewController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var Util = require('framework/Util');
    var jQuery = require('jquery');

    var NCarousel = require('libs/NCarousel/NCarousel');

    var CollectionsDataFeed = require('app/libs/CollectionsDataFeed');
    var collectionTemplate = require('text!app/views/collection.html');
    var collectionVideoDrawerTemplate = require('text!app/views/collection-video-drawer.html');
    var collectionPaginationTemplate = require('text!app/views/collection-pagination.html');

    var CollectionViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);

            return this;
        },

        _initConfig: function() {
            this.base();

            var config = this._config;

            config.filterChangeRefreshDelay = 1000;
            config.containerOpenHeight = 213;
        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;

            references.dataFeed = new CollectionsDataFeed();

            references.$collectionsWrapper = $referenceBase;
            references.$loadingIndicator = $referenceBase.find('.js-loading-indicator');
            references.$collectionsContainer = $referenceBase.find('.js-collections-container');
            references.$paginationContainers = $referenceBase.find('.js-pagination');
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.currentPageNumber = 0;

            // these are set to home page defaults here
            state.collectionsPerPage = 12;
            state.collectionsPerRow = 4;
            state.videoDrawerClasses = '';
            state.videosPerDrawer = 5;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            // data processed
            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            // input param changed alert from data feed
            boundFunctions.onInputParamChanged = this._onInputParamChanged.bind(this);
            references.dataFeed.on('inputParamChanged', boundFunctions.onInputParamChanged)

            // collection rendering events
            boundFunctions.onCollectionItemClick = this._onCollectionItemClick.bind(this);
            references.$collectionsContainer.on('click', '.js-collection-item', boundFunctions.onCollectionItemClick);

            // collection pagination
            boundFunctions.onPaginationItemClick = this._onPaginationItemClick.bind(this);
            references.$collectionsWrapper.find('.js-pagination').on('click', '.js-pagination-item', boundFunctions.onPaginationItemClick);
        },

        setCollectionsPerPage: function(n) {
            this._state.collectionsPerPage = n;
            return this;
        },

        setCollectionsPerRow: function(n) {
            this._state.collectionsPerRow = n;
            return this;
        },

        setVideoDrawerClasses: function(classes) {
            this._state.videoDrawerClasses = classes;
            return this;
        },

        setVideosPerDrawer: function(n) {
            this._state.videosPerDrawer = n;
            return this;
        },

        getCollections: function(page, collectionsPerPage) {

            if (page == undefined) {
                page = this._state.currentPageNumber;
            } else {
                this._state.currentPageNumber = page;
            }

            if (collectionsPerPage == undefined) {
                collectionsPerPage = this._state.collectionsPerPage;
            } else {
                this._state.collectionsPerPage = collectionsPerPage;
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('page', page, true)
            dataFeed.setInputParam('count', collectionsPerPage, true);

            var collectionsArray = dataFeed.getCollections();
            var totalCount = dataFeed.getTotalCount();

            if (collectionsArray == false) {
                return false;
            }

            this._updateCollectionsDisplay(collectionsArray, totalCount);
        },

        _onDataProcessed: function() {
            this.getCollections();
        },

        _updateCollectionsDisplay: function(collectionsArray, totalCount) {

            this._renderCollections(collectionsArray);
            this._renderPagination(totalCount);
            this._initVideoCarousels();

            this._references.$loadingIndicator.hide();

            var broadcastData = {
                totalCount: totalCount
            };

            this.trigger('collectionsUpdated', broadcastData);
        },

        _initVideoCarousels: function() {
            var $carouselWrappers = this._references.$collectionsContainer.find('.js-carousel-wrapper');

            var i = 0;
            var len = $carouselWrappers.length;
            for (; i < len; i++) {
                new NCarousel($carouselWrappers.eq(i), {
                    autoPlay: false,
                    allowWrapping: false
                });
            }
        },






        _renderCollections: function(collectionsArray, totalCount) {
            // local references
            var state = this._state;
            var collectionsPerRow = state.collectionsPerRow;
            var videoDrawerClasses = state.videoDrawerClasses;

            var entireRenderedHTML = '';

            var tempVideoDrawerArray = [];

            var i = 0;
            var j;
            var len = collectionsArray.length;
            for (; i < len; i++) {
                var currentCollectionData = Util.Object.clone(collectionsArray[i], true);
                currentCollectionData._index = i;
                currentCollectionData._collectionStats = this._getCollectionStats(currentCollectionData);
                currentCollectionData._plural = (currentCollectionData.videos.length != 1);

                // render collections
                entireRenderedHTML += viewRenderer.render(collectionTemplate, currentCollectionData);
                
                // add length to each video
                for (j = 0; j < currentCollectionData.videos.length; j++) {
                    currentCollectionData.videos[j]._time = Util.secondsToHMSFormat(currentCollectionData.videos[j].duration);
                }

                // organize videos into slides
                var videoDrawerData = this._prepareVideoDrawerData(currentCollectionData.videos);
                
                // assign remaining needed rendering data
                videoDrawerData._index = i;

                // store the video drawer data
                tempVideoDrawerArray.push(videoDrawerData);

                // once we've displayed our desired amount of videos in this column.
                // include accumulated video drawer html with the overall html
                if ((i + 1) % collectionsPerRow == 0 || i == len - 1) {
                    entireRenderedHTML += viewRenderer.render(collectionVideoDrawerTemplate, {
                        _videoDrawerClasses: videoDrawerClasses,
                        _videoDrawers: tempVideoDrawerArray
                    });

                    tempVideoDrawerArray.splice(0);
                }
            }

            this._references.$collectionsContainer.html(entireRenderedHTML);
        },

        _getCollectionStats: function(collectionData) {
            var time = 0;
            var adoptions = 0;
            var views = 0;
            var likes = 0;

            var videos = collectionData.videos;

            if (!videos) {
                throw new Error('CollectionViewController._getCollectionStats(): trying to get collection stats on an object with no videos array');
            }

            var i = 0;
            var len = videos.length;
            for (; i < len; i++) {
                var currentVideo = videos[i];

                time += currentVideo.duration;
                adoptions += currentVideo.adoptions;
                views += currentVideo.offlineViews + currentVideo.onlineViews;
                likes += currentVideo.offlineLikes + currentVideo.onlineLikes;
            }

            return {
                time: Util.secondsToHMSFormat(time),
                adoptions: Util.integerCommaFormat(adoptions),
                views: Util.integerCommaFormat(views),
                likes: Util.integerCommaFormat(likes)
            };
        },

        _prepareVideoDrawerData: function(videos) {

            var videosPerDrawer = this._state.videosPerDrawer;

            var carouselSlides = [];

            var i = 0;
            var len = videos.length;
            var j;
            var slideVideos;
            for (; i < len; i += videosPerDrawer) {
                slideVideos = [];
                for (j = 0; j < videosPerDrawer && j + i < len; j++) {
                    var currentVideo = videos[i + j];
                    currentVideo._videoIndex = j + 1;
                    slideVideos.push(currentVideo);
                }
                carouselSlides.push({
                    videos: slideVideos
                });
            }

            return {
                carouselSlides: carouselSlides
            };
        },

        _renderPagination: function(totalCount) {
            var collectionsPerPage = this._state.collectionsPerPage;
            var pages = Math.ceil(totalCount / collectionsPerPage);

            var paginationPages = [];
            var i = 0;
            for (; i < pages; i++) {

                var currentPageData = {
                    pageIndex: i,
                    pageNumber: i + 1
                };

                if (i == this._state.currentPageNumber) {
                    currentPageData.classes = 'selected';
                }

                paginationPages.push(currentPageData);
            }

            var renderedPagination = viewRenderer.render(collectionPaginationTemplate, {pages: paginationPages});

            this._references.$paginationContainers.html(renderedPagination);
        },

        _onPaginationItemClick: function(e) {
            e.preventDefault();

            var $currentTarget = jQuery(e.currentTarget);
            var pageIndex = $currentTarget.data('pageIndex');

            // if we're already viewing the page clicked, no need to continue
            if (pageIndex == this._state.currentPageNumber) {
                return;
            }

            var $paginationItems = this._references.$paginationContainers.find('.js-pagination-item');
            $paginationItems.removeClass('selected');

            var $selectedItems = $paginationItems.filter('[data-page-index=' + pageIndex + ']');
            $selectedItems.addClass('selected');

            this._references.$loadingIndicator.show();
            this.getCollections(pageIndex);
        },

        _onCollectionItemClick: function(e) {
            var $collectionItem = jQuery(e.currentTarget);

            var collectionItemIndex = $collectionItem.data('collectionItemIndex');

            var $videoDrawerContainers = this._references.$collectionsContainer.find('.js-video-container');
            var $videoDrawers = $videoDrawerContainers.find('.js-video-drawer');

            var $currentDrawer;
            var i = 0;
            var len = $videoDrawers.length;

            for (; i < len; i++) {
                var $tempVideoDrawer = $videoDrawers.eq(i);
                if ($tempVideoDrawer.data('parentCollectionItemIndex') == collectionItemIndex) {
                    $currentDrawer = $tempVideoDrawer;
                    break;
                }
            }

            var $currentVideoDrawerContainer = $currentDrawer.closest('.js-video-container');
            var $videoDrawersToHide = $currentVideoDrawerContainer
                .find('.js-video-drawer')
                .not($currentDrawer);

            var containerAlreadyOpen = $currentVideoDrawerContainer.hasClass('open');
            if (!containerAlreadyOpen) {
                // animate the desired container open
                this._openVideoDrawerContainers($currentVideoDrawerContainer);

                // animate any containers aside from our to-be-open container closed
                this._closeVideoDrawerContainers($videoDrawerContainers.not($currentVideoDrawerContainer));
            }

            // display the desired drawer
            this._showDrawers($currentDrawer);

            // hide any other drawers
            this._hideDrawers($videoDrawersToHide);
            

            // position the pointer
            var $drawerPointer = $currentVideoDrawerContainer.find('.js-pointer');

            var collectionItemLeftOffset = $collectionItem.offset().left;
            var collectionItemWidth = $collectionItem.width();

            var currentDrawerLeftOffset = $currentDrawer.offset().left;

            var drawerPointerWidth = $drawerPointer.width();

            
            var staticOffset = 20;

            var newLeftPosition = (collectionItemLeftOffset - currentDrawerLeftOffset) + (collectionItemWidth / 2) - (drawerPointerWidth / 2) + staticOffset;

            if (containerAlreadyOpen) {
                $drawerPointer.animate({
                    left: newLeftPosition + 'px'
                });
            } else {
                $drawerPointer.css('left', newLeftPosition);
            }
        },

        _openVideoDrawerContainers: function($videoDrawerContainers) {
            $videoDrawerContainers
                .stop(true)
                .animate({
                    height: this._config.containerOpenHeight + 'px'
                })
                .addClass('open');
        },

        _closeVideoDrawerContainers: function($videoDrawerContainers) {
            $videoDrawerContainers
                .stop(true)
                .animate({
                    height: '0px'
                })
                .removeClass('open');
        },

        _showDrawers: function($drawer) {
            $drawer.css({
                position: 'relative',
                visibility: 'visible'
            });
        },

        _hideDrawers: function($drawer) {
            $drawer.css({
                position: '',
                visibility: ''
            });
        },

        setInputParam: function(key, value, disableCacheClearing) {
            this._references.dataFeed.setInputParam(key, value, disableCacheClearing);
        },

        setFilterStatus: function(filterParam, filterValue, active) {
            this._references.dataFeed.setFilterStatus(filterParam, filterValue, active);
        },

        clearFilters: function() {
            if (!this._references.dataFeed.clearFilters()) {
                return;
            }

            this._onSearchCriteriaChanged();
        },

        _onInputParamChanged: function() {
            this._onSearchCriteriaChanged();
        },

        _onSearchCriteriaChanged: function() {
            this._references.$loadingIndicator.show();
            this.getCollections(0);
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

    return CollectionViewController;
});
