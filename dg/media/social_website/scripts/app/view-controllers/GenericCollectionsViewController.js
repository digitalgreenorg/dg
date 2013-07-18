/**
 * GenericCollectionsViewController Class File
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

    var collectionWrapperTemplate = require('text!app/views/collection-wrapper.html');
    var collectionTemplate = require('text!app/views/collection.html');
    var collectionVideoDrawerTemplate = require('text!app/views/collection-video-drawer.html');


    var GenericCollectionsViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase, params) {
            this.base($referenceBase, params);

            return this;
        },

        _initConfig: function() {
            this.base();

            var config = this._config;

            config.containerOpenHeight = 213;
        },

        _initReferences: function($referenceBase, params) {
            this.base($referenceBase, params);

            var references = this._references;

            references.collectionsDataFeeds = {};
            references.$collectionsWrapper = $referenceBase;
        },

        _initEvents: function(params) {
            this.base(params);

            var references = this._references;
            var boundFunctions = this._boundFunctions;
            var references = this._references;

            // collection rendering events
            boundFunctions.onCollectionItemClick = this._onCollectionItemClick.bind(this);
            references.$collectionsWrapper.on('click', '.js-collection-item', boundFunctions.onCollectionItemClick);

            boundFunctions.totalNumberOfCollectionsReachedBinds = {};
            var currentTotalNumberOfCollectionsReachedBind;
            var k;
            for (k in references.collectionsDataFeeds) {
                currentTotalNumberOfCollectionsReachedBind = this._onTotalNumberOfCollectionsReached.bind(this, k);
                boundFunctions.totalNumberOfCollectionsReachedBinds[k] = currentTotalNumberOfCollectionsReachedBind;
                references.collectionsDataFeeds[k].on('totalNumberOfCollectionsReached', currentTotalNumberOfCollectionsReachedBind);
            }
        },

        _initState: function(params) {
            this.base(params);

            var state = this._state;

            state.collectionsPerRow = -1;
            // these are set to home page defaults here
            state.collectionsPerPage = -1;
            state.videoDrawerClasses = '';
            state.videosPerDrawer = -1;
        },

        _addCollectionsDataFeed: function(id, dataFeed) {
            this._references.collectionsDataFeeds[id] = dataFeed;
        },

        _setCurrentCollectionsDataFeed: function(id) {
            var references = this._references;
            var currentCollectionsDataFeed = references.collectionsDataFeeds[id];

            if (currentCollectionsDataFeed == undefined) {
                throw new Error('GenericCollectionsViewController._setCurrentCollectionsDataFeed(): no data feed found with id: "' + id + '"');
            }

            references.currentCollectionsDataFeed = currentCollectionsDataFeed;
        },

        _getCurrentCollectionDataFeed: function() {
            var currentCollectionsDataFeed = this._references.currentCollectionsDataFeed;

            if (currentCollectionsDataFeed == undefined) {
                throw new Error('GenericCollectionsViewController._getCurrentCollectionDataFeed(): no "currentCollectionsDataFeed" reference set');
            }

            return currentCollectionsDataFeed;
        },

        _setAllCollectionsInputParam: function(name, value) {
            var collectionsDataFeeds = this._references.collectionsDataFeeds;
            var id;
            for (id in collectionsDataFeeds) {
                collectionsDataFeeds[id].setInputParam(name, value);
            }

            return this;
        },

        setCollectionsPerRow: function(n) {
            this._state.collectionsPerRow = n;
            return this;
        },

        setCollectionsPerPage: function(n) {
            this._state.collectionsPerPage = n;
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

        _setCollectionsPage: function(pageDescriptor) {
            var currentCollectionsDataFeed = this._getCurrentCollectionDataFeed();
            currentCollectionsDataFeed.setCollectionsPage(pageDescriptor);
        },

        _getCollectionsPage: function(pageDescriptor) {
            var currentCollectionsDataFeed = this._getCurrentCollectionDataFeed();
            var collectionsPageData = currentCollectionsDataFeed.getCollectionsPage(pageDescriptor, undefined, this._onCollectionsPageReceived.bind(this));
            return collectionsPageData;
        },

        _onCollectionsPageReceived: function(collectionsData) {
            var collectionsHTML = this._generateCollectionHTML(collectionsData);
            this._renderPartialCollections(collectionsHTML);
        },

        _getAllCurrentCollectionsPages: function() {
            var currentCollectionsDataFeed = this._getCurrentCollectionDataFeed();
            var allCurrentCollectionsPagesData = currentCollectionsDataFeed.getAllCurrentCollectionsPages();
            this._onAllCollectionsReceived(allCurrentCollectionsPagesData);
            return allCurrentCollectionsPagesData;
        },

        _onAllCollectionsReceived: function(collectionsData) {
            var collectionsHTML = this._generateCollectionHTML(collectionsData);
            this._renderAllCollections(collectionsHTML);
        },

        _onTotalNumberOfCollectionsReached: function(collectionId, feedInformation) {},

        _onCollectionItemClick: function(e) {

            var $collectionItem = jQuery(e.currentTarget);

            var collectionItemIndex = $collectionItem.data('collectionItemIndex');

            var $videoDrawerContainers = this._references.$collectionsWrapper.find('.js-video-container');
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
        
        _generateCollectionHTML: function(collectionsData, totalCount) {

            var state = this._state;

            var collectionsPerRow = state.collectionsPerRow;
            if (collectionsPerRow == undefined) {
                throw new Error('GenericCollectionsViewController._generateCollectionHTML(): the number of collections per row is not set; call setCollectionsPerRow() prior to attempting to fetch data');
            }

            var videoDrawerClasses = state.videoDrawerClasses;

            var collectionsArray = collectionsData.collections;

            var entireRenderedHTML = '';
            var tempRenderHTML = '';

            var tempVideoDrawerArray = [];

            var i = 0;
            var j;
            var len = collectionsArray.length;
            for (; i < len; i++) {
                var currentCollectionData = Util.Object.clone(collectionsArray[i], true);

                var itemIndex = (collectionsData.startPage * collectionsData.countPerPage) + i
                currentCollectionData._index = itemIndex;
                currentCollectionData._collectionStats = this._getCollectionStats(currentCollectionData);
                currentCollectionData._plural = (currentCollectionData.videos.length != 1);

                // render collections
                tempRenderHTML += viewRenderer.render(collectionTemplate, currentCollectionData);
                
                // add length to each video
                for (j = 0; j < currentCollectionData.videos.length; j++) {
                    currentCollectionData.videos[j]._time = Util.secondsToHMSFormat(currentCollectionData.videos[j].duration);
                }

                // organize videos into slides
                var videoDrawerData = this._prepareVideoDrawerData(currentCollectionData.videos);
                
                // assign remaining needed rendering data
                videoDrawerData._index = itemIndex;

                // store the video drawer data
                tempVideoDrawerArray.push(videoDrawerData);

                // once we've displayed our desired amount of videos in this column.
                // include accumulated video drawer html with the overall html
                if ((i + 1) % collectionsPerRow == 0 || i == len - 1) {
                    tempRenderHTML += viewRenderer.render(collectionVideoDrawerTemplate, {
                        _videoDrawerClasses: videoDrawerClasses,
                        _videoDrawers: tempVideoDrawerArray
                    });

                    var $wrapper = jQuery('<div />');
                    $wrapper.html(collectionWrapperTemplate);

                    $wrapper.find('.js-collections-page').html(tempRenderHTML);
                    entireRenderedHTML += $wrapper.html();

                    tempVideoDrawerArray.splice(0);
                    tempRenderHTML = '';
                }
            }

            return entireRenderedHTML;
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

        _renderPartialCollections: function(collectionHTML) {
            throw new Error('GenericCollectionsViewController._renderPartialCollections(): abstract function not overridden or this.base() called');
        },

        _renderAllCollections: function(collectionHTML) {
            throw new Error('GenericCollectionsViewController._renderAllCollections(): abstract function not overridden or this.base() called');
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

    return GenericCollectionsViewController;
});
