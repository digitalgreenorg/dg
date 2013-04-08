/**
 * FollowDataFeed Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');

    var FollowDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            // NOTE: response code testing; only one is required for implementation
            this.base('api/genericReturnOK.php');
            // this.base('api/genericReturnError.php');
            
            this.addInputParam('userID', true);
            this.addInputParam('activityId', true);
        },

        fetch: function(activityId, userID, customCallback) {
            this.setInputParam('userID', userID);
            this.setInputParam('activityId', activityId);

            this.base(null, customCallback);
        },

        _initConfig: function() {
            this.base();
            this._config.fetchDelay = 0;
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
        }
    });

    return FollowDataFeed;

});