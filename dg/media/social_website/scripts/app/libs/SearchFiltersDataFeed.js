/**
 * SearchFiltersDataFeed Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');

    var SearchFiltersDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            this.base('api/searchFilters');
        },

        _initConfig: function() {
            this.base();
            this._config.fetchDelay = 0;
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            // no data formatting/processing need be done; simply store it
            this._dataModel.set('searchFilters', unprocessedData);
            return unprocessedData;
        },

        getSearchFilters: function() {
            return this._dataModel.get('searchFilters');
        }

    });

    return SearchFiltersDataFeed;

});