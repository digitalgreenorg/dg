/**
 * ViewCollectionsController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var Util = require('framework/Util');
    var jQuery = require('jquery');

    require('libs/external/swfobject/swfobject');

    var VideoLikeDataFeed = require('app/libs/VideoLikeDataFeed');
    var CommentDataFeed = require('app/libs/CommentsDataFeed');
    //var CommentLikeDataFeed = require('app/libs/CommentLikeDataFeed');
    //var TimeWatchedDataFeed = require('app/libs/TimeWatchedDataFeed');

    var CommentsFeedViewController = require('app/view-controllers/CommentsFeedViewController');

    var NCarousel = require('libs/NCarousel/NCarousel');
    
    var ViewCollectionsController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {ViewCollectionsController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            this._initVideoPlayer();
            this._initVideoStats();

            this._getComments();
        },

        _initConfig: function() {
            // how often we should update the server with video watched info in ms
    //        this._config.updateVideoWatchedTimeDelay = 5000;
        },

        _initReferences: function() {
            this.base();

            var references = this._references;

            references.$commentsAreaWrapper = jQuery('.js-comments-feed-wrapper');
            references.commentsFeedViewController = new CommentsFeedViewController(references.$commentsAreaWrapper);

            references.videoLikeDataFeed = new VideoLikeDataFeed();
            references.commentDataFeed = new CommentDataFeed();
      // 	uncomment when comment-like and user time watched functionality is updated  
      //      references.commentLikeDataFeed = new CommentLikeDataFeed();
      //      references.timeWatchedDataFeed = new TimeWatchedDataFeed();

            references.$likeButton = jQuery('.js-like-button');
            references.$commentBox = jQuery('#comment');
            references.$commentButton = jQuery('.comment-btn');

            references.$videoTarget = jQuery('#video-target');

            var $videosCarouselWrapper = jQuery('#collection-videos-carousel');
            references.videosCarousel = new NCarousel($videosCarouselWrapper, {
                autoPlay: false,
                allowWrapping: false
            });
        },

        _initEvents: function() {
            this.base();

            var references = this._references;
            var boundFunctions = this._boundFunctions;
            
            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.videoLikeDataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            boundFunctions.onLikeButtonClick = this._onVideoLikeButtonClick.bind(this);
            references.$likeButton.on('click', boundFunctions.onLikeButtonClick);

            boundFunctions.onCommentButtonClick = this._onCommentButtonClick.bind(this);
            references.$commentButton.on('click', boundFunctions.onCommentButtonClick);
            
            boundFunctions.onCommentLikeButtonClick = this._onCommentLikeButtonClick.bind(this);
            references.$commentsAreaWrapper.on('click', '.js-comment-like-button', boundFunctions.onCommentLikeButtonClick);
        },

        _initState: function() {
            this.base();

            var state = this._state;

            state.videoLiked = false;

            // get user id
            // get video id
            state.userID = jQuery('body').data('userId');
            state.videoUID = this._references.$videoTarget.data('video-uid');

            this._references.videoLikeDataFeed.fetch(state.videoUID, state.userID);
            state.videoLiked = this._state.videoLiked;
            
            state.updateVideoWatchedTimeInterval = undefined;
            this._references.videosCarousel.moveToSlide(parseInt(($('.video-wrapper').attr('data-videoid')-1)/5),{stopAutoPlay: false});
        },

        _initVideoStats: function() {
            
            var $statBarWrappers = jQuery('.js-stat-bar-wrapper');
            var $statBar;
            var $leftValue;
            var $rightValue;
            var $statIndicator;

            var i = 0;
            var len = $statBarWrappers.length;
            for (; i < len; i++) {
                var $currentStatBarWrapper = $statBarWrappers.eq(i);

                $statBar = $currentStatBarWrapper.find('.js-stat-bar');
                var leftValue = $statBar.data('leftValue');
                var rightValue = $statBar.data('rightValue');

                $leftValue = $currentStatBarWrapper.find('.js-left-value');
                $rightValue = $currentStatBarWrapper.find('.js-right-value');
                $leftValue.html(Util.integerCommaFormat(leftValue));
                $rightValue.html(Util.integerCommaFormat(rightValue));

                $statIndicator = $currentStatBarWrapper.find('.js-stat-indicator');

                // for basic width setting, use this line instead
                // $statIndicator.css('width', ((leftValue * 100) / (leftValue + rightValue)) + '%');

                // otherwise, this can be used to animate the effect
                $statIndicator.animate({
                    width: ((leftValue * 100) / (leftValue + rightValue)) + '%'
                }, 2000);

            }
        },

        _initVideoPlayer: function() {

            var videoId = this._references.$videoTarget.data('videoId');

            var params = { allowScriptAccess: "always" };
            var atts = { id: "video-player" };
            swfobject.embedSWF(
                'http://www.youtube.com/v/' + videoId + '?enablejsapi=1&playerapiid=ytplayer&version=3',
                'video-target',
                '703',
                '395',
                '8',
                null,
                null,
                params,
                atts
            );

            window.onYouTubePlayerReady = this._onYouTubePlayerReady.bind(this);
        },

        _onYouTubePlayerReady: function() {
            // clean up the window
            window.onYouTubePlayerReady = undefined;

            var videoPlayer = jQuery('#video-player').get(0);
            this._references.videoPlayer = videoPlayer;

            // youtube seems to force us to put functions in the window
            // we'll do our best to handle that elegantly
            window.onYouTubePlayerStateChange = this._onYouTubePlayerStateChange.bind(this);

            videoPlayer.addEventListener('onStateChange', 'onYouTubePlayerStateChange');
            
            // The id that is shown in the URL. Below functionality will autoplay the youtube video on all video pages except for the first video in a collection
            var videoId = jQuery('.video-wrapper').attr('data-videoid');
            if (videoId != 1){
            	videoPlayer.playVideo();
            }
        },

        _onYouTubePlayerStateChange: function(newState) {
            switch (newState) {
                // playback completed/stopped
                case 0:
                    var now_playing_video = jQuery('.now-playing').closest('li');
                    var next_video = now_playing_video.next();
                    if (next_video.length == 0) {
                        /* End of current slide or this is the last video altogether */
                        var next_slide = now_playing_video.closest('ul').closest('li').next();
                        if (next_slide.length == 0) {
                            /* Last video - go back to the first video */
                            next_slide = now_playing_video.closest('ul').closest('li').closest('ul').find('li:first');
                        }
                        next_video = next_slide.find('ul > li:first-child');
                    }
                    window.location.href = next_video.find('.vidDrawer-image a').attr('href');
                // stop the interval and manually send an update
                case 2:
                    this._stopUpdateInterval();
                    this._updateVideoWatchedTime();
                    break;
                // playback started
                case 1:
                    this._startUpdateInterval();
                    break;
            }
        },

        _startUpdateInterval: function() {
            // ensure we don't orphan an interval
            this._stopUpdateInterval();

            this._state.updateVideoWatchedTimeInterval = setInterval(this._updateVideoWatchedTime.bind(this), this._config.updateVideoWatchedTimeDelay);
        },

        _stopUpdateInterval: function() {
            clearInterval(this._state.updateVideoWatchedTimeInterval);
            this._state.updateVideoWatchedTimeInterval = null;
        },

        _updateVideoWatchedTime: function() {
            var videoUID = this._state.videoUID;
            var userID = this._state.userID;
            // we use the current time as our indicator of how much of the video has been watched
            // NOTE: this will not account for seeking; if the user seeks to the end, it will appear
            // as if they watched the entire video
            
            //uncomment when functionality is available
            //var timeWatched = this._references.videoPlayer.getCurrentTime();
            //this._references.timeWatchedDataFeed.fetch(videoUID, userID, Math.floor(timeWatched));
        },

        _getComments: function() {
            this._references.commentsFeedViewController.getComments();
        },
        
        

        _onDataProcessed: function(likedEntries) {
            this._state.videoLiked = likedEntries[0].liked;
            if (this._state.videoLiked) {
                this._references.$likeButton.addClass('liked');
            }
        },
        
        _onVideoLikeButtonClick: function(e) {
            e.preventDefault();

            if (this._state.videoLiked) {
                return;
            }

            var $currentTarget = jQuery(e.currentTarget);

            var videoUID = this._state.videoUID;
            var userID = this._state.userID;

            if (videoUID == undefined || userID == undefined) {
                throw new Error('ViewCollectionsController._onVideoLikeButtonClick: videoUID and userID are required parameters');
            }

            this._references.videoLikeDataFeed.fetch(videoUID, userID, function(){}, 'POST');
        },

        _onCommentButtonClick: function(e) {
            e.preventDefault();

            var $currentTarget = jQuery(e.currentTarget);

            var videoUID = this._state.videoUID;
            var userID = this._state.userID;
            var text = this._references.$commentBox.val();

            if (videoUID == undefined || userID == undefined || text == undefined) {
                throw new Error('ViewCollectionsController._onCommentButtonClick: videoUID ,userID, text are required parameters');
            }

            this._references.commentDataFeed.addInputParam('video', false, videoUID);
            this._references.commentDataFeed.addInputParam('user', false, userID);
            this._references.commentDataFeed.addInputParam('text', false, text);
            
            this._references.commentDataFeed.setInputParam('video', videoUID, true);
            this._references.commentDataFeed.setInputParam('user', userID, true);
            this._references.commentDataFeed.setInputParam('text', text, true);
            
            this._references.commentDataFeed._fetch(null, this._onVideoLikedCallback.bind(this), 'POST');
        },
        
        _onCommentLikeButtonClick: function(e) {
            e.preventDefault();

            if (this._state.videoLiked) {
                return;
            }

            var $currentTarget = jQuery(e.currentTarget);

            var commentUID = $currentTarget.data('commentUid');
            var commentLiked = $currentTarget.data('commentLiked');
            var userID = this._state.userID;

            if (commentUID == undefined || userID == undefined || commentLiked == undefined) {
                throw new Error('ViewCollectionsController._onVideoLikeButtonClick: commentUID, userID, and commentLiked are required parameters');
            }

            var newCommentLikedStatus = !(commentLiked == '1');

            this._references.commentLikeDataFeed.fetch(commentUID, userID, newCommentLikedStatus, this._onCommentLikedCallback.bind(this, $currentTarget, newCommentLikedStatus));
        },

        _onVideoLikedCallback: function() {
            var responseStatus = this._references.videoLikeDataFeed.getResponseStatus();

            if (responseStatus.success) {
                this._references.$likeButton.addClass('liked');
                this._state.videoLiked = true;
            } else {
                // NOTE: any desired error handling would go here
            }
        },

        _onCommentLikedCallback: function($commentLikeButton, newCommentLikedStatus, data) {
            var responseStatus = this._references.commentLikeDataFeed.getResponseStatus();

            if (responseStatus.success) {

                if (newCommentLikedStatus) {
                    $commentLikeButton
                        .addClass('liked')
                        .data('commentLiked', (newCommentLikedStatus) ? '1' : '0');

                    var likedCount = data.likedCount || 0;

                    $commentLikeButton.find('.js-like-count').html(Util.integerCommaFormat(likedCount));
                    $commentLikeButton.find('.js-like-label').html((likedCount != 1) ? 'Likes' : 'Like');
                } else {
                    $commentLikeButton
                        .removeClass('liked')
                        .data('commentLiked', (newCommentLikedStatus) ? '1' : '0');
                }
                
            } else {
                // NOTE: any desired error handling would go here
            }
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return ViewCollectionsController;
});
