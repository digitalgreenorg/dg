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

    var FeaturedCollectionDataFeed = require('app/libs/FeaturedCollectionDataFeed');
    var featuredCollectionTemplate = require('text!app/views/featured-collection.html');

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

            references.dataFeed = new FeaturedCollectionDataFeed();

            //references.$newsItemsWrapper = $referenceBase;
            //references.$newsItemsContainer = $referenceBase.find('.js-news-feed-container');
            //references.$newsFeedShowMoreButton = $referenceBase.find(".js-news-feed-show-more-btn");
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.currentLanguage = Util.Cookie.get('language__name');
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            //pulling more info
            
        },

        

        

        

        getFeaturedCollection: function(language) {

            /*if (language == undefined) {
                language = this.get;
            } else {
                this.setCurrentLanguage(language);
            }*/

                        
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('language__name', language, true)
           

            var featuredcollectionData = dataFeed.getFeaturedCollection();
            

            if(featuredcollectionData == false){
                return false;
            }

            this._renderFeaturedCollection(featuredcollectionData);
        },

        _onDataProcessed: function() {
            this.getFeaturedCollection();
        },

        _renderFeaturedCollection: function(featuredcollectionData) {

            var renderData = {
                featuredcollection: featuredcollectionData
            };
            var $featuredCollectionsContainer = jQuery(".js-featured-collections-wrapper");

            var renderedFeaturedCollection = viewRenderer.render( featuredCollectionTemplate,featuredcollectionData );
            $featuredCollectionsContainer.html(renderedFeaturedCollection);
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
