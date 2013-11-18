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

        /*
        Input params:
        activityUID|videoUID {Number}
        page {Number}
        count {Number}

        Output params:
        comments {Comment[]}
        totalCount {Number}
        */

        constructor: function() {
            this.base('api/video/');

            // prepare data model
            var collectionVideoDropDownSubModel = this._dataModel.addSubModel('collectionVideoDropDown', true);
            
            //will move it to view controller
            /*this.addInputParam('offset', false, 0);
            this.addInputParam('limit', false, 10);
            this.addInputParam('video', false,jQuery('.featured-ft-videoDetails').attr('data-video-uid'));*/
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
                this.clearCommentCache();
            }

            return paramChanged;
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