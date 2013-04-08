/**
 * CommentLikeDataFeed Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');

    var CommentLikeDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            this.base('api/commentLike.php');
            
            this.addInputParam('commentUID', true);
            this.addInputParam('userID', true);
            this.addInputParam('liked', true);
        },

        fetch: function(commentUID, userID, liked, customCallback) {
            this.setInputParam('commentUID', commentUID);
            this.setInputParam('userID', userID);
            this.setInputParam('liked', liked);

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

    return CommentLikeDataFeed;

});