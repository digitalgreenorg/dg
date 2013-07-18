/**
 * FeaturedCollectionViewController Class File
 *
 * @author aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    
    var FeaturedCollectionDataFeed = DigitalGreenDataFeed.extend({

        /*
         * Input params:
         * language {string}
         * 
         * Output params: featuredCollection {FeaturedCollection}
         * 
         */

        constructor: function($language) {
            this.base('api/featuredCollection/');

            // prepare data model
            var featuredCollectionsSubModel = this._dataModel.addSubModel('featuredCollection', true);
            this.addInputParamCacheClear('language__name',
            		featuredCollectionsSubModel);
        },

        fetch: function(language) {
            this.setInputParam('language__name', language, true);
            
            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var featuredCollectionModel = dataModel.get('featuredCollection');
            
            featuredCollectionModel.set('featuredCollectionObj', unprocessedData.featured_collection);
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearFeaturedCollectionCache();
            }

            return paramChanged;
        },

        clearFeaturedCollectionCache: function() {
            this._dataModel.get('featuredCollection').clear();
        },

        getFeaturedCollection: function() {
            var language = this.getInputParam('language__name');
            var featuredCollectionModel = this._dataModel.get('featuredCollection');
            var featuredCollection = featuredCollectionModel.get('featuredCollectionObj');

            if (!featuredCollection) {
                this.fetch(language);
                return false;
            }
            return featuredCollection;
        }

    });

    return FeaturedCollectionDataFeed;

});