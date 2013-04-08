/**
 * VideoLikeDataFeed Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');

    var VideoLikeDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            // NOTE: response code testing; only one is required for implementation
            this.base('api/genericReturnOK.php');
            // this.base('api/genericReturnError.php');
            
            this.addInputParam('videoUID', true);
            this.addInputParam('userID', true);
        },

        fetch: function(videoUID, userID, customCallback) {
            this.setInputParam('videoUID', videoUID);
            this.setInputParam('userID', userID);

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

    return VideoLikeDataFeed;

});