/**
 * PracticeMappingDataFeed Class File
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
    
    var AnalyticsDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/getthedeo/');

            // prepare data model
            var analyticsSubModel = this._dataModel.addSubModel('analytics', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var analyticsModel = dataModel.get('analytics');
            
            analyticsModel.set('analyticsObj', unprocessedData.analytics);
            return unprocessedData.analytics;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearanalyticsCache();
            }

            return paramChanged;
        },

        clearanalyticsCache: function() {
            this._dataModel.get('analytics').clear();
        },

        getAnalytics: function() {
            var analyticsModel = this._dataModel.get('analytics');
            var analytics = analyticsModel.get('analyticsObj');

            if (!analytics) {
                this.fetch();
                return false;
            }
            return analytics;
        }

    });

    return AnalyticsDataFeed;

});