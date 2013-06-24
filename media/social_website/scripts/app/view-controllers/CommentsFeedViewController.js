/**
 * CommentsFeedViewController Class File
 *
 * @author dlakes
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var Util = require('framework/Util');
    var jQuery = require('jquery');

    var CommentsDataFeed = require('app/libs/CommentsDataFeed');
    var commentTemplate = require('text!app/views/comment.html');

    var CommentsFeedViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);

            return this;
        },

        _initConfig: function() {
            this.base();

        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;

            references.dataFeed = new CommentsDataFeed();

            references.$commentsAreaWrapper = $referenceBase;
            references.$commentsList = $referenceBase.find('.js-comment-list');
            references.$commentsFeedShowMoreButton = $referenceBase.find(".js-comments-show-more-btn");
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.currentPageNumber = 0;
            state.commentsPerPage = 10;
            state.currentCount = 0;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            //pulling more info
            boundFunctions.onShowMoreClick = this._onShowMoreClick.bind(this);
            references.$commentsFeedShowMoreButton.on("click", boundFunctions.onShowMoreClick);

            // show/hide replies
            boundFunctions.onToggleRepliesClick = this._onToggleRepliesClick.bind(this);
            references.$commentsList.on('click', '.js-reply-visibility-toggle', boundFunctions.onToggleRepliesClick);
        },

        setCommentsPerPage: function(n) {
            this._state.commentsPerPage = n;
            return this;
        },

        getCommentsPerPage: function(){
            return this._state.commentsPerPage;
        },

        setCurrentPageNumber: function(n) {
            this._state.currentPageNumber = n;
            return this;
        },

        getCurrentPageNumber: function(){
            return this._state.currentPageNumber;
        },

        getComments: function(page, commentsPerPage) {

            if (page == undefined) {
                page = this.getCurrentPageNumber();
            } else {
                this.setCurrentPageNumber(page);
            }

            if (commentsPerPage == undefined) {
                commentsPerPage = this.getCommentsPerPage();
            } else {
                this.setCommentsPerPage(commentsPerPage)
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('offset', page*commentsPerPage, true)
            dataFeed.setInputParam('limit', commentsPerPage, true);

            var commentsArray = dataFeed.getComments();
            var totalCount = dataFeed.getTotalCount();

            if(commentsArray == false){
                return false;
            }

            this._updateCommentsFeedDisplay(commentsArray, totalCount);
        },

        _onDataProcessed: function() {
            this.getComments();
        },

        _updateCommentsFeedDisplay: function(commentsArray, totalCount) {
            this._renderComments(commentsArray);
            this._onCommentsFeedUpdated(totalCount, commentsArray.length);
        },

        _onCommentsFeedUpdated: function(totalCount, addedCount) {
            this.updateTotalCount(totalCount);
            this.addToCurrentCount(addedCount);
            this.updateCommentsItemPaginationDisplay();
        },

        _renderComments: function(commentsArray) {

            // Commenting user and changing to farmer for every comment
        	//var userID = jQuery('body').data('userId');
        	
            
            var renderCommentsArray = [];

            var i = 0;
            var len = commentsArray.length;
            var j;
            var repliesLength;
            for (; i < len; i++) {
                var currentCommentsItemData = Util.Object.clone(commentsArray[i], true);
                var farmer = currentCommentsItemData.farmer;
                
                //commenting replies amd like comment code
                
                /*currentCommentsItemData._repliesPlural = currentCommentsItemData.replies.length != 1;
                currentCommentsItemData._formattedLikedCount = Util.integerCommaFormat(currentCommentsItemData.likedCount);
                currentCommentsItemData._likesPlural = currentCommentsItemData.likedCount != 1;
                currentCommentsItemData._replied = false;

                // loop through replies to see if the current user has replied
                var replies = currentCommentsItemData.replies;
                j = 0;
                repliesLength = replies.length;
                for (; j < repliesLength; j++) {
                    var currentReply = replies[j];

                    if (currentReply.user.uid == userID) {
                        currentCommentsItemData._replied = true;
                    }

                    currentReply._formattedLikedCount = Util.integerCommaFormat(currentReply.likedCount);
                    currentReply._likesPlural = currentReply.likedCount != 1;
                }
                */

                renderCommentsArray.push(currentCommentsItemData);
            }

            var renderData = {
                comments: renderCommentsArray
            };

            viewRenderer.renderAppend(this._references.$commentsList, commentTemplate, renderData);
        },

        updateTotalCount: function(totalCount) {
            this._state.totalCount = totalCount;
            jQuery('.js-comment-count').html(Util.integerCommaFormat(totalCount));
        },

        addToCurrentCount: function(numNewItems){
            this._state.currentCount += numNewItems;
        },

        updateCommentsItemPaginationDisplay: function(){
            if(this._state.currentCount >= this._state.totalCount){
                this._references.$commentsFeedShowMoreButton.hide();
            }
        },

        _onShowMoreClick: function(event){
            event.preventDefault();
            event.stopPropagation();
            this.getComments(this.getCurrentPageNumber() + 1)
        },

        _onToggleRepliesClick: function(e) {
            e.preventDefault();

            var $comment = jQuery(e.currentTarget).closest('.js-comment');
            var $replyContainer = $comment.find('.js-reply-container');

            // init the element
            if ($replyContainer.data('fullHeight') == undefined) {
                $replyContainer
                    .data('fullHeight', $replyContainer.height())
                    .css('height', '0px')
                    .css('display', 'block');
            }

            if ($replyContainer.hasClass('expanded')) {
                $replyContainer
                    .stop(true)
                    .animate({
                        height: '0px'
                    }, 1000)
                    .removeClass('expanded');
            } else {
                $replyContainer
                    .stop(true)
                    .animate({
                        height: $replyContainer.data('fullHeight') + 'px'
                    }, 1000)
                    .addClass('expanded');
            }
        },

        setInputParam: function(key, value, disableCacheClearing) {
            if (!this._references.dataFeed.setInputParam(key, value, disableCacheClearing)) {
                return;
            }
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();

            // TODO: clean up
        }
    });

    return CommentsFeedViewController;
});
