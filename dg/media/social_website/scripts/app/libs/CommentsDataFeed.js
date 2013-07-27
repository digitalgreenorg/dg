/**
 * CommentsDataFeed Class File
 *
 * @author dlakes
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    var Util = require('framework/Util');

    var CommentsDataFeed = DigitalGreenDataFeed.extend({

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
            this.base('api/comment/');

            // prepare data model
            this._dataModel.addSubModel('objects', true);

            this.addInputParam('offset', false, 0);
            this.addInputParam('limit', false, 10);
            this.addInputParam('video', false,jQuery('.featured-ft-videoDetails').attr('data-video-uid'));
        },

        fetch: function(page, countPerPage, customCallback) {
            if (page == undefined) {
                page = 0;
            }

            if (countPerPage == undefined) {
                countPerPage = 12;
            }

            this.setInputParam('offset', page, true);
            this.setInputParam('limit', countPerPage, true);
            this.setInputParam('video', jQuery('.featured-ft-videoDetails').attr('data-video-uid') , true);

            // perform the fetch
            this.base();
            
            this.base(null, customCallback);
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            // If this was a post of a comment, then an object is returned not an array.
            if (unprocessedData.objects == undefined) {
                if (unprocessedData.uid != undefined) {
                    /* Clear cache so next fetch includes this newly added comment. */
                    this.clearCommentCache();
                    var commentsToAdd = [];
                    return commentsToAdd;
                }
            }
            
            // local references
            var dataModel = this._dataModel;
            var commentsModel = dataModel.get('objects');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.meta.limit;
            var page = unprocessedData.meta.offset;

            // store total count
            dataModel.set('totalCount', unprocessedData.meta.total_count);

            // import comments from data
            var commentsToAdd = unprocessedData.objects;
            var startingCacheId = page * countPerPage;

            commentsModel.addSubset(commentsToAdd, startingCacheId);
            return commentsToAdd;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearCommentCache();
            }

            return paramChanged;
        },

        clearCommentCache: function() {
            this._dataModel.get('objects').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getComments: function() {

            var page = this.getInputParam('offset');
            var countPerPage = this.getInputParam('limit');

            var comments = this._dataModel.get('objects').getSubset(page * countPerPage, countPerPage);

            if (!comments) {
                this.fetch(page, countPerPage);
                return false;
            }

            return comments;
        }

    });

    return CommentsDataFeed;

});