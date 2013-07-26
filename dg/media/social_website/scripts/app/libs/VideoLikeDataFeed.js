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
            this.base('api/updateVideoLike/');
            // this.base('api/genericReturnError');
            
            this.addInputParam('video', true);
            this.addInputParam('user', true);
        },

        fetch: function(videoUID, userID, customCallback, type) {
            this.setInputParam('video', videoUID);
            this.setInputParam('user', userID);

            this.base(null, customCallback, type);
        },

        _initConfig: function() {
            this.base();
            this._config.fetchDelay = 0;
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            return unprocessedData;
        }
    });

    return VideoLikeDataFeed;

});