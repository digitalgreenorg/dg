/**
 * HomeController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
$(document).ready(function(){
	// Fixed image will be used instead of creating canvas for featured collection
	// 
	
	/*var c=document.getElementById("myCanvas");
	var ctx=c.getContext("2d");
	var img=$(".mosaic").each(function(){
		if(this.id==1){
			ctx.drawImage(this,0,0,100,50);	
			}
		else if(this.id==2){
			ctx.drawImage(this,200,0,130,250);
			}
		else if(this.id==3){
			ctx.drawImage(this,100,0,100,50);
			}
		else if(this.id==4){
			ctx.drawImage(this,0,50,100,200);
			}
		else if(this.id==5){
			ctx.drawImage(this,100,50,100,200);
			}
			
			});*/
	});

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var CollectionViewController = require('app/view-controllers/CollectionViewController');
    var CollectionMostFiltersViewController = require('app/view-controllers/CollectionMostFiltersViewController');
    var NewsFeedViewController = require('app/view-controllers/news/NewsFeedViewController');
    var FeaturedCollectionViewController = require('app/view-controllers/FeaturedCollectionViewController');
    var jQuery = require('jquery');

    var NCarousel = require('libs/NCarousel/NCarousel');

    var HomeController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {HomeController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            var references = this._references;

            references.collectionViewController
                .setCollectionsPerPage(12)
                .setCollectionsPerRow(4)
                .setVideosPerDrawer(5);

            // set the active filter to be Most Liked to init the collections
            references.collectionMostFiltersViewController.setActiveFilter('-likes');
            
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
            references.$mainCarouselWrapper = jQuery('#main-carousel');

            references.mainCarousel = new NCarousel(references.$mainCarouselWrapper, {
                transition: 'slide',
                autoPlay: true,
                autoPlayDelay: 8000
            });
        },

        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onOrderChanged = this._onOrderChanged.bind(this);
            references.collectionMostFiltersViewController.on('orderChanged', boundFunctions.onOrderChanged);

            boundFunctions.onNewsFeedUpdated = this._onNewsFeedUpdated.bind(this);
            references.newsFeedViewController.on('newsFeedUpdated', boundFunctions.onNewsFeedUpdated);
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
