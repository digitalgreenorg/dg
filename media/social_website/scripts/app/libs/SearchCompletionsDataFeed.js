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

    var SearchCompletionsDataFeed = DigitalGreenDataFeed.extend({

        /*
        Input params:

        searchString {String}
        maxCount {Number}

        Output params:
        completions {SearchCompletion[]}
        totalCount {Number}
        */

        constructor: function() {
            this.base('api/searchCompletions.php');

            // prepare data model
            this._dataModel.addSubModel('searchCompletions', true);

            this.addInputParam('searchString', true, '');
            this.addInputParam('maxCount', false, 10);
        },

        fetch: function(searchString, maxCount) {
            if (searchString == undefined) {
                searchString = 0;
            }

            if (maxCount == undefined) {
                maxCount = 10;
            }

            this.setInputParam('searchString', searchString, true);
            this.setInputParam('maxCount', maxCount, true);

            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var searchCompletionsModel = dataModel.get('searchCompletions');

            // import news from data
            var searchCompletionsToAdd = unprocessedData.completions;

            searchCompletionsModel.clear();
            searchCompletionsModel.addSubset(searchCompletionsToAdd, 0);
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearSearchCompletionCache();
            }

            return paramChanged;
        },

        clearSearchCompletionCache: function() {
            this._dataModel.get('searchCompletions').clear();
        },

        getSearchItems: function() {
            var searchString = this.getInputParam('searchString');
            var maxCount = this.getInputParam('maxCount');

            var searchCompletions = this._dataModel.get('searchCompletions').getSubset(0, maxCount);

            if (!searchCompletions) {
                this.fetch(searchString, maxCount);
                return false;
            }

            return searchCompletions;
        }

    });

    return SearchCompletionsDataFeed;

});