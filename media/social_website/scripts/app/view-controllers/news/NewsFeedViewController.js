/**
 * NewsFeedViewController Class File
 *
 * @author dlakes
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

    var NewsDataFeed = require('app/libs/NewsDataFeed');
    var newsItemTemplate = require('text!app/views/news/newsItem.html');

    var NewsFeedViewController = Controller.extend({

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

        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;

            references.dataFeed = new NewsDataFeed();

            references.$newsItemsWrapper = $referenceBase;
            references.$newsItemsContainer = $referenceBase.find('.js-news-feed-container');
            references.$newsFeedShowMoreButton = $referenceBase.find(".js-news-feed-show-more-btn");
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.currentPageNumber = 0;
            state.newsItemsPerPage = 10;
            state.currentCount = 0;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            //pulling more info
            boundFunctions.onShowMoreClick = this._onShowMoreClick.bind(this);
            references.$newsFeedShowMoreButton.on("click", boundFunctions.onShowMoreClick);
        },

        setNewsItemsPerPage: function(n) {
            this._state.newsItemsPerPage = n;
            return this;
        },

        getNewsItemsPerPage: function(){
            return this._state.newsItemsPerPage;
        },

        setCurrentPageNumber: function(n) {
            this._state.currentPageNumber = n;
            return this;
        },

        getCurrentPageNumber: function(){
            return this._state.currentPageNumber;
        },

        getNewsItems: function(page, newsItemsPerPage) {

            if (page == undefined) {
                page = this.getCurrentPageNumber();
            } else {
                this.setCurrentPageNumber(page);
            }

            if (newsItemsPerPage == undefined) {
                newsItemsPerPage = this.getNewsItemsPerPage();
            } else {
                this.setNewsItemsPerPage(newsItemsPerPage)
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('page', page, true)
            dataFeed.setInputParam('count', newsItemsPerPage, true);

            var activitiesData = dataFeed.getNewsItems();
            var totalCount = dataFeed.getTotalCount();

            if(activitiesData == false){
                return false;
            }

            this._updateNewsFeedDisplay(activitiesData, totalCount);
        },

        _onDataProcessed: function() {
            this.getNewsItems();
        },

        _updateNewsFeedDisplay: function(activitiesData, totalCount) {
            this._prepareData(activitiesData);
            this._renderNewsItems(activitiesData);

            var broadcastData = {
                totalCount: totalCount,
                addedCount: activitiesData.length
            };

            this.trigger('newsFeedUpdated', broadcastData);
        },

        _renderNewsItems: function(activitiesData) {

            var renderData = {
                activities: activitiesData
            };

            viewRenderer.renderAppend(this._references.$newsItemsContainer, newsItemTemplate, renderData);

            this._initCarousels();

        },

        _initCarousels: function() {
            var $carouselWrappers = this._references.$newsItemsContainer.find('.js-carousel-wrapper');

            var i = 0;
            var len = $carouselWrappers.length;
            for (; i < len; i++) {
                new NCarousel($carouselWrappers.eq(i), {
                    autoPlay: false,
                    allowWrapping: false
                });
            }
        },

        _prepareData: function(activitiesData) {
            // TODO: add in additional things here (video count, time, etc.)

            var i = 0;
            var len = activitiesData.length;
            for (; i < len; i++) {
                var currentActivity = activitiesData[i];

                currentActivity._hasImages = (currentActivity.images && currentActivity.images.length != 0);
                currentActivity._hasComments = currentActivity.comments.length != 0;
                currentActivity._likes = Util.integerCommaFormat(currentActivity.likes);

                if (currentActivity.collection && currentActivity.collection.videos) {

                    var videos = currentActivity.collection.videos;

                    var collectionStats = {
                        likes: 0,
                        views: 0,
                        adoptions: 0,
                        time: 0
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

                        if ((j > 0 && (j + 1) % 4 == 0) || j == videosLen - 1) {
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











        updateTotalCount: function(totalCount) {
            this._state.totalCount = totalCount;
        },

        addToCurrentCount: function(numNewItems){
            this._state.currentCount += numNewItems;
        },

        updateNewsItemPaginationDisplay: function(){
            if(this._state.currentCount >= this._state.totalCount){
                this._references.$newsFeedShowMoreButton.hide();
            }
        },

        _onShowMoreClick: function(event){
            event.preventDefault();
            event.stopPropagation();
            this.getNewsItems(this.getCurrentPageNumber() + 1)
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

    return NewsFeedViewController;
});
