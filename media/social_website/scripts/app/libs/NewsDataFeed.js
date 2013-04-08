/**
 * NewsDataFeed Class File
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

    var NewsDataFeed = DigitalGreenDataFeed.extend({

        /*
        Input params:

        page {Number}
        count {Number}

        Output params:
        newsItems {Activity[]}
        totalCount {Number}
        */

        constructor: function() {
            this.base('api/newsFeed.php');

            // prepare data model
            this._dataModel.addSubModel('newsItems', true);

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
            var newsItemsModel = dataModel.get('newsItems');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.requestParameters.count;
            var page = unprocessedData.requestParameters.page;

            // store total count
            dataModel.set('totalCount', unprocessedData.totalCount);

            // import news from data
            var newsItemsToAdd = unprocessedData.newsItems;
            var startingCacheId = page * countPerPage;

            newsItemsModel.addSubset(newsItemsToAdd, startingCacheId);
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearNewsItemCache();
            }

            return paramChanged;
        },

        clearNewsItemCache: function() {
            this._dataModel.get('newsItems').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getNewsItems: function() {

            var page = this.getInputParam('page');
            var countPerPage = this.getInputParam('count');

            var newsItems = this._dataModel.get('newsItems').getSubset(page * countPerPage, countPerPage);

            if (!newsItems) {
                this.fetch(page, countPerPage);
                return false;
            }

            return newsItems;
        }

    });

    return NewsDataFeed;

});