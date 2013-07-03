/**
 * FeaturedCollectionViewController Class File
 *
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
    var FeaturedCollectionDataFeed = require('app/libs/FeaturedCollectionDataFeed');
    var featuredCollectionTemplate = require('text!app/views/featured-collection.html');

    var FeaturedCollectionViewController = Controller.extend({

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
            references.$featuredCollectionContainer = $referenceBase
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
        },

        getFeaturedCollection: function(language) {
            if (language == undefined) {
                language = Util.Cookie.get('language__name');
            }
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
            var renderedFeaturedCollection = viewRenderer.render( featuredCollectionTemplate,featuredcollectionData );
            this._references.$featuredCollectionContainer.html(renderedFeaturedCollection);
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

    return FeaturedCollectionViewController;
});
