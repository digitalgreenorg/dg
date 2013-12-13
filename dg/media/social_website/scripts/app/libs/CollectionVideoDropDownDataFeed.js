/**
 * CollectionVideoDropDownDataFeed Class File
 *
 * @author Aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    var Util = require('framework/Util');

    var CollectionVideoDropDownDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            this.base('api/video/');

            // prepare data model
            var collectionVideoDropDownSubModel = this._dataModel.addSubModel('collectionVideoDropDown', true);
            
        },

        fetch: function() {
            // perform the fetch
        	this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var collectionDropDownModel = dataModel.get('collectionVideoDropDown');

            collectionDropDownModel.set('collectionDropDownObj', unprocessedData.objects);
            return unprocessedData.objects;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearVideoDropDownCache();
            }

            return paramChanged;
        },

        clearVideoDropDownCache: function() {
            this._dataModel.get('collectionVideoDropDown').clear();
        },

        getCollectionVideoDropDown: function() {

        	var collectionDropDownModel = this._dataModel.get('collectionVideoDropDown');
            var collectionDropDown = collectionDropDownModel.get('collectionDropDownObj');

            if (!collectionDropDown) {
                this.fetch();
                return false;
            }
            return collectionDropDown;
        
        }
        

    });

    return CollectionVideoDropDownDataFeed;

});