/**
 * ActivitiesViewController Class File
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

    var activitiesDataFeed = require('app/libs/ActivitiesDataFeed');
    var activityTemplate = require('text!app/views/profile/activity.html');

    var collectionVideoDrawerTemplate = require('text!app/views/collection-video-drawer.html');

    var ActivitiesViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);
            
            this.getActivities();

            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;
            // data feed
            references.dataFeed = new activitiesDataFeed();

            // html element references
            references.$activitiesWrapper = $referenceBase;
            references.$activitiesContainer = $referenceBase.find('.js-activities-container');
            references.$activitiesShowMoreButton = $referenceBase.find(".js-activities-show-more-btn");
            
        },
        _initState: function() {
            this.base();

            var state = this._state;
            state.currentPageNumber = 0;
            state.activitiesPerPage = 10;
            state.currentCount = 0;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);
            
            boundFunctions.onShowMoreClick = this._onShowMoreClick.bind(this);
            references.$activitiesShowMoreButton.on("click", boundFunctions.onShowMoreClick);
        },
        
        setActivitiesPerPage: function(n) {
            this._state.activitiesPerPage = n;
            return this;
        },

        getActivitiesPerPage: function(){
            return this._state.activitiesPerPage;
        },

        setCurrentPageNumber: function(n) {
            this._state.currentPageNumber = n;
            return this;
        },

        getCurrentPageNumber: function(){
            return this._state.currentPageNumber;
        },

        _onDataProcessed: function() {
            this.getActivities();
        },

        getActivities: function(page, activitiesPerPage) {

        	if (page == undefined) {
                page = this.getCurrentPageNumber();
            } else {
                this.setCurrentPageNumber(page);
            }

            if (activitiesPerPage == undefined) {
                activitiesPerPage = this.getActivitiesPerPage();
            } else {
                this.setActivitiesPerPage(activitiesPerPage)
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('offset', page, true)
            dataFeed.setInputParam('limit', activitiesPerPage, true);

            var activitiesData = dataFeed.getActivities();
            var totalCount = dataFeed.getTotalCount();

            if (activitiesData == false) {
                return false;
            }

            this._prepareData(activitiesData);
            this._renderActivities(activitiesData);
        },

        _prepareData: function(activitiesData) {
            // TODO: add in additional things here (video count, time, etc.)

            var i = 0;
            var len = activitiesData.length;
            for (; i < len; i++) {
                var currentActivity = activitiesData[i];

                currentActivity._hasImages = (currentActivity.images && currentActivity.images.length != 0);
                //currentActivity._hasComments = currentActivity.comments.length != 0;
                //currentActivity._likes = Util.integerCommaFormat(currentActivity.likes);

                if (currentActivity.collection && currentActivity.collection.videos) {

                    var videos = currentActivity.collection.videos;

                    var collectionStats = {
                        likes: 0,
                        views: 0,
                        adoptions: 0,
                        totalDuration: 0
                    };

                    var carouselSlides = [];
                    var carouselSlide = [];

                    var j = 0;
                    var videosLen = videos.length;
                    for (; j < videosLen; j++) {
                        var currentVideo = videos[j];

                        collectionStats.likes += (currentVideo.offlineLikes + currentVideo.onlineLikes);
                        collectionStats.views += (currentVideo.offlineViews + currentVideo.onlineViews);
                        collectionStats.adoptions += currentVideo.adoptions;
                        collectionStats.totalDuration += currentVideo.duration;

                        carouselSlide.push(currentVideo);

                        if ((j > 0 && (j + 1) % 3 == 0) || j == videosLen - 1) {
                            carouselSlides.push({
                                videos: carouselSlide
                            });
                            carouselSlide = [];
                        }
                    }

                    currentActivity.collection._carouselSlides = carouselSlides;

                    // format
                    collectionStats.likes = Util.integerCommaFormat(collectionStats.likes);
                    collectionStats.views = Util.integerCommaFormat(collectionStats.views);
                    collectionStats.adoptions = Util.integerCommaFormat(collectionStats.adoptions);
                    collectionStats.totalDuration = Util.secondsToHMSFormat(collectionStats.totalDuration);

                    currentActivity.collection._collectionStats = collectionStats;
                }
            }
        },

        _renderActivities: function(activitiesData) {

            var renderData = {
                activities: activitiesData
            };

            viewRenderer.renderAppend(this._references.$activitiesContainer, activityTemplate, renderData);

            this._initCarousels();
            stButtons.locateElements();
        },

        _initCarousels: function() {
            var $carouselWrappers = this._references.$activitiesContainer.find('.js-carousel-wrapper');

            var i = 0;
            var len = $carouselWrappers.length;
            for (; i < len; i++) {
                new NCarousel($carouselWrappers.eq(i), {
                    autoPlay: false,
                    allowWrapping: false
                });
            }
        },

        _onShowMoreClick: function(event){
            event.preventDefault();
            event.stopPropagation();
            this.getActivities(this.getCurrentPageNumber() + 1)
        },
        
        setInputParam: function(key, value, disableCacheClearing) {
            if (!this._references.dataFeed.setInputParam(key, value, disableCacheClearing)) {
                return;
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

    return ActivitiesViewController;
});
