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
            this.base('api/comment.php');

            // prepare data model
            this._dataModel.addSubModel('comments', true);

            this.addInputParam('page', false, 0);
            this.addInputParam('count', false, 10);
        },

        fetch: function(page, countPerPage) {
            if (page == undefined) {
                page = 0;
            }

            if (countPerPage == undefined) {
                countPerPage = 12;
            }

            this.setInputParam('page', page, true);
            this.setInputParam('count', countPerPage, true);

            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var commentsModel = dataModel.get('comments');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.requestParameters.count;
            var page = unprocessedData.requestParameters.page;

            // store total count
            dataModel.set('totalCount', unprocessedData.totalCount);

            // import comments from data
            var commentsToAdd = unprocessedData.comments;
            var startingCacheId = page * countPerPage;

            commentsModel.addSubset(commentsToAdd, startingCacheId);
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearCommentCache();
            }

            return paramChanged;
        },

        clearCommentCache: function() {
            this._dataModel.get('comments').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getComments: function() {

            var page = this.getInputParam('page');
            var countPerPage = this.getInputParam('count');

            var comments = this._dataModel.get('comments').getSubset(page * countPerPage, countPerPage);

            if (!comments) {
                this.fetch(page, countPerPage);
                return false;
            }

            return comments;
        }

    });

    return CommentsDataFeed;

});