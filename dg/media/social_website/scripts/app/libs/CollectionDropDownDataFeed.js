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
    
    var CollectionDropDownDataFeed = DigitalGreenDataFeed.extend({

        /*
         * Input params:
         * 
         * Output params: featuredCollection {FeaturedCollection}
         * 
         */

        constructor: function($language) {
            this.base('api/mapping/');

            // prepare data model
            var collectionDropDownSubModel = this._dataModel.addSubModel('collectionDropDown', true);
            //this.addInputParamCacheClear('language__name',
            //		featuredCollectionsSubModel);
        },

        fetch: function(language) {
            //this.setInputParam('language__name', language, true);
            
            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var collectionDropDownModel = dataModel.get('collectionDropDown');
            
            collectionDropDownModel.set('collectionDropDownObj', unprocessedData.mapping_dropdown);
            return unprocessedData.mapping_dropdown;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearCollectionDropDownCache();
            }

            return paramChanged;
        },

        clearCollectionDropDownCache: function() {
            this._dataModel.get('collectionDropDown').clear();
        },

        getCollectionDropDown: function() {
            //var language = this.getInputParam('language__name');
            var collectionDropDownModel = this._dataModel.get('collectionDropDown');
            var collectionDropDown = collectionDropDownModel.get('collectionDropDownObj');

            if (!collectionDropDown) {
                this.fetch();
                return false;
            }
            return collectionDropDown;
        }

    });

    return CollectionDropDownDataFeed;

});