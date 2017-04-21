/**
 * HomeController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('controllers/DigitalGreenPageController');
    var CollectionViewController = require('app/view-controllers/CollectionViewController');
    var CollectionMostFiltersViewController = require('app/view-controllers/CollectionMostFiltersViewController');
    var NewsFeedViewController = require('app/view-controllers/news/NewsFeedViewController');
    var FeaturedCollectionViewController = require('app/view-controllers/FeaturedCollectionViewController');
    var jQuery = require('jquery');

    var NCarousel = require('libs/NCarousel/NCarousel');
    
    require('libs/external/swfobject/swfobject');

    var HomeController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {HomeController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            var references = this._references;

            references.collectionViewController
                .setCollectionsPerPage(4)
                .setCollectionsPerRow(4)
                .setVideosPerDrawer(5);

            // set the active filter to be Most Liked to init the collections
            references.collectionMostFiltersViewController.setActiveFilter('-featured');
            
            this._getNewsFeed();
            this._getFeaturedCollection();

            return this;
        },

        _initReferences: function($referenceBase) {
            this.base($referenceBase);

            var references = this._references;

            var $collectionsContainer = jQuery('.js-collections-wrapper');
            var $newsFeedContainer = jQuery(".js-news-feed-wrapper");
            var $featuredCollectionContainer = jQuery(".js-featured-collection-wrapper");

            // helpers
            var $languageCookie = Util.Cookie.get('language__name');
            references.collectionViewController = new CollectionViewController($collectionsContainer, $languageCookie);
            references.collectionMostFiltersViewController = new CollectionMostFiltersViewController($collectionsContainer);
            references.newsFeedViewController = new NewsFeedViewController($newsFeedContainer);
            references.FeaturedCollectionViewController = new FeaturedCollectionViewController($featuredCollectionContainer, $languageCookie);

            // dom elements
            references.$imageCarouselWrapper = jQuery('.js-imageCarousel');

            references.imageCarousel = new NCarousel(references.$imageCarouselWrapper, {
                transition: 'fade',
                autoPlay: true,
                autoPlayDelay: 2000
            });
            
            // play button 
            references.$playButton = jQuery('.play-button');

            // awards ticker
            references.$awardsTicker = jQuery('.js-awards-ticker');
            references.$awardsTickerLeftArrow =jQuery('.js-awards-left-arrow');
            references.$awardsTickerRightArrow =jQuery('.js-awards-right-arrow');
            references.$awardsElements = jQuery('.js-description');
            references.$investorTicker = jQuery('.js-investor-ticker');

        },

        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onOrderChanged = this._onOrderChanged.bind(this);
            references.collectionMostFiltersViewController.on('orderChanged', boundFunctions.onOrderChanged);

            boundFunctions.onNewsFeedUpdated = this._onNewsFeedUpdated.bind(this);
            references.newsFeedViewController.on('newsFeedUpdated', boundFunctions.onNewsFeedUpdated);
            
            boundFunctions.onPlayButtonClick = this._onVideoPlayButtonClick.bind(this);
            references.$playButton.on('click', boundFunctions.onPlayButtonClick);

            boundFunctions.onAwardsLeftClick = this._onAwardsLeftClick.bind(this);
            references.$awardsTickerLeftArrow.on('click', boundFunctions.onAwardsLeftClick)

            boundFunctions.onAwardsRightClick = this._onAwardsRightClick.bind(this);
            references.$awardsTickerRightArrow.on('click', boundFunctions.onAwardsRightClick)

            boundFunctions.onAwardsElementClick = this._onAwardsElementClick.bind(this);
            references.$awardsElements.on('click', boundFunctions.onAwardsElementClick);

            //boundFunctions.playInvestorTicker = this._playInvestorTicker.bind(this);
            //references.$investorTicker.on('load', boundFunctions.playInvestorTicker);
            this._playInvestorTicker();
        },

        _onOrderChanged: function(orderCriteria) {
            this._references.collectionViewController.setInputParam('order_by', orderCriteria);
        },

        _getCollections: function() {
            this._references.collectionViewController.getCollections();
        },

        _getNewsFeed: function() {
            this._references.newsFeedViewController.getNewsItems();
        },

        _getFeaturedCollection: function() {
        	this._references.FeaturedCollectionViewController.getFeaturedCollection();
        },
        _onNewsFeedUpdated: function (broadcastData){
            this._references.newsFeedViewController.updateTotalCount(broadcastData.totalCount);
            this._references.newsFeedViewController.addToCurrentCount(broadcastData.addedCount);
            this._references.newsFeedViewController.updateNewsItemPaginationDisplay();
        },
        
        _initVideoPlayer: function() {
            // This code loads the IFrame Player API code asynchronously and place the script tag before 
            // all other script tags.
            var tag = document.createElement('script');
            tag.src = "https://www.youtube.com/iframe_api";
            var firstScriptTag = document.getElementsByTagName('script')[0];
            firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
            var player;
            window.onYouTubeIframeAPIReady = this._onYouTubeIframeAPIReady.bind(this);
            window.onYouTubePlayerReady = this._onYouTubePlayerReady.bind(this);
            $("#video-img > div").not("#player").each(function(index, ele){$(ele).hide();});
            $("#player").show();
        },

        _onYouTubeIframeAPIReady: function() {
            window.onPlayerReady = this._onPlayerReady.bind(this);
            window.onPlayerStateChange = this._onPlayerStateChange.bind(this);
            player = new YT.Player('player', {
                height: '424',
                width: '1024',
                videoId: 'JYkaf4ucaSc',
                autoplay : 1,
                events: {
                  'onReady': onPlayerReady,
                  'onStateChange': onPlayerStateChange
                }
            });
        },

        _onPlayerReady: function(e) {
            $('.slide-img').hide();
            $('.player').show();
            e.target.playVideo();
        },

        _onPlayerStateChange: function() {
            var done = false;
            if (event.data == YT.PlayerState.PLAYING && !done) {
                done = true;
            }
        },

        stopVideo: function() {
            player.stopVideo();
        },


        _onYouTubePlayerReady: function() {
            // clean up the window
            window.onYouTubePlayerReady = undefined;

            var videoPlayer = jQuery('#player').get(0);
            this._references.videoPlayer = videoPlayer;

            // youtube seems to force us to put functions in the window
            // we'll do our best to handle that elegantly
            window.onYouTubePlayerStateChange = this._onYouTubePlayerStateChange.bind(this);

            videoPlayer.addEventListener('onStateChange', 'onYouTubePlayerStateChange');
            
            videoPlayer.playVideo();
            
        },

        _onYouTubePlayerStateChange: function(newState) {
            if (newState == 0){
            	$("#player").hide();          
				$("#video-img > div").not("#player").each(function(index, ele){$(ele).show();});
            }
        	
        },
        
        _onVideoPlayButtonClick: function(e) {
        	this._initVideoPlayer();
        },

        _onAwardsLeftClick: function(e){
            var that=this
                var width = that._references.$awardsTicker.children().first().width() + 16; // compensate for margins
                var lastChild = that._references.$awardsTicker.children().last();
                that._references.$awardsTicker.prepend(lastChild);
                that._references.$awardsTicker.css({'left': '-'+width+'px'});
                that._references.$awardsTicker.animate({left: '+'+0+'px'},400,'swing', function(){
                    $('.js-awards-description-show').removeClass('js-awards-description-show');
                    var data = that._references.$awardsTicker.children().first().attr('data');
                    $('.js-awards-description').each(function(index, element) {
                        if($(this).attr('data') == data) $(this).addClass('js-awards-description-show');
                    });
                });
        },

        _onAwardsRightClick: function(e){
            var that=this
                var width = that._references.$awardsTicker.children().first().width() + 16; // compensate for margins
                that._references.$awardsTicker.animate({left:'-'+width+'px'},400,'swing', function(){
                    that._references.$awardsTicker.append(that._references.$awardsTicker.children().first());
                    that._references.$awardsTicker.css({'left':'0px'});
                    $('.js-awards-description-show').removeClass('js-awards-description-show');
                    var data = that._references.$awardsTicker.children().first().attr('data');
                    $('.js-awards-description').each(function(index, element) {
                        if($(this).attr('data') == data) $(this).addClass('js-awards-description-show');
                    });
                });
        },

        _onAwardsElementClick: function(e){
            var element = e.currentTarget;
            var data = element.getAttribute('data');
            $('.js-awards-description-show').removeClass('js-awards-description-show');
            $('.js-awards-description').each(function(index, element) {
                if($(this).attr('data') == data) $(this).addClass('js-awards-description-show');
            });
        },

        _playInvestorTicker: function(){
            var that=this;
            console.log("here");
            setInterval(function(){
                var width = that._references.$investorTicker.children().first().width() + 26; // compensate for margins
                that._references.$investorTicker.animate({left:'-'+width+'px'},3000,'linear', function() {
                    that._references.$investorTicker.append(that._references.$investorTicker.children().first());
                    that._references.$investorTicker.css({'left':'0px'});
                });
            }, 3000);
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return HomeController;
});
