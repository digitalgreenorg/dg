define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    var Util = require('framework/Util');

    var FeaturedCollectionDataFeed = DigitalGreenDataFeed.extend({

        
        /*Input params:

        language {string}
        

        Output params:
        featuredCollection {Activity[]}
        */
        

        constructor: function() {
            this.base('api/featuredCollection/');

            // prepare data model
            this._dataModel.addSubModel('featuredCollection', true);
            this.addInputParam('language__name', false, Util.Cookie.get('language__name'));
        },

        fetch: function(language) {
            if (language == undefined) {
                language = Util.Cookie.get('language__name');  //set from cookie
            }
            this.setInputParam('language__name', language, true);
            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var featuredCollectionModel = dataModel.get('featuredCollection');
            featuredCollectionModel.set('1',unprocessedData.featured_collection);  //1 is the key with which this data will be fetched
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
            var featuredCollection = featuredCollectionModel.get('1');  //1 was set in process data

            if (!featuredCollection) {
                this.fetch(language);
                return false;
            }
            return featuredCollection;
        }

    });

    return FeaturedCollectionDataFeed;

});