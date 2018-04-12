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
        
        _onFetchError: function(error) {
            this.base(error);
            if(error.status == 401){
                var url = "/login/?next=" + window.location.pathname
                window.location.assign(url)
            }
        },

        _initConfig: function() {
            this.base();
            this._config.fetchDelay = 0;
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            if (unprocessedData.objects == undefined) {
                if (unprocessedData.id != undefined) {
                    return [{
                      'liked': true
                    }];
                }
                return [{
                  'liked': false
                }];
            }
            var likedEntries = unprocessedData.objects;
            if (likedEntries.length > 0) {
                return [{
                  'liked': true
                }];
            }
            return [{
              'liked': false
            }];
        }
    });

    return VideoLikeDataFeed;

});