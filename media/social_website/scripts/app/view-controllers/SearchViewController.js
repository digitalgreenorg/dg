/**
 * NewsFeedViewController Class File
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

    var SearchCompletionsDataFeed = require('app/libs/SearchCompletionsDataFeed');
    var searchCompletionTemplate = require('text!app/views/searchCompletion.html');

    var SearchViewController = Controller.extend({

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

            this._config.searchInputChangeRefreshDelay = 1000;
        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;

            references.dataFeed = new SearchCompletionsDataFeed();

            references.$searchWrapper = $referenceBase;
            references.$searchInputBox = $referenceBase.find('input#search');
            references.$searchItemsContainer = $referenceBase.find('.js-search-items-container');
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.maxCount = 10;
            state.searchInputVal = "";
            state.searchInputChangedTimeout = undefined;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            // prevent default & stop propagation
            boundFunctions.preventDefaultStopPropagation = function(e) {
                e.preventDefault();
                e.stopPropagation();
            };
            references.$searchWrapper.on('click', boundFunctions.preventDefaultStopPropagation);

            // data processed
            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            // on key down
            boundFunctions.onKeyDown = this._onKeyDown.bind(this);
            references.$searchInputBox.keydown(boundFunctions.onKeyDown);

            // on key up
            boundFunctions.onKeyUp = this._onKeyUp.bind(this);
            references.$searchInputBox.keyup(boundFunctions.onKeyUp);

            // on search item mouse enter
            boundFunctions.onSearchItemMouseEnter = this._onSearchItemMouseEnter.bind(this);
            references.$searchItemsContainer.on('mouseenter', '.js-search-completion-item', boundFunctions.onSearchItemMouseEnter);

            // search input timeout
            boundFunctions.onSearchInputChangedTimeout = this._onSearchInputChangedTimeout.bind(this);

            // body click
            boundFunctions.onBodyClick = this._onBodyClick.bind(this);
            jQuery('body').on('click', boundFunctions.onBodyClick);
        },

        setMaxCount: function(n) {
            this._state.maxCount = n;
            return this;
        },

        getMaxCount: function(){
            return this._state.maxCount;
        },

        setSearchInputVal: function(value){
            this._state.searchInputVal = value;
            return this;
        },

        getSearchInputVal: function(){
            return this._state.searchInputVal;
        },

        getSearchItems: function(term, maxCount) {
            if (maxCount == undefined) {
                maxCount = this.getMaxCount();
            } else {
                this.setMaxCount(maxCount)
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('searchString', term, true);
            dataFeed.setInputParam('maxCount', maxCount, true);

            var searchItemsArray = dataFeed.getSearchItems();

            if(searchItemsArray == false){
                return false;
            }

            this._updateSearchDisplay(searchItemsArray);
        },

        _onDataProcessed: function() {
            this.getSearchItems();
        },

        _updateSearchDisplay: function(searchItemsArray) {

            // format the data how we'll need it
            var categories = [];

            var i = 0;
            var j;
            var len = searchItemsArray.length;
            var categoryReference;

            for (; i < len; i++) {
                categoryReference = undefined;
                
                for (j = 0; j < categories.length; j++) {
                    if (categories[j].type == searchItemsArray[i].type) {
                        categoryReference = categories[j];
                        break;
                    }
                }

                if (categoryReference == undefined) {
                    var categoryReference = {
                        type: searchItemsArray[i].type,
                        items: []
                    };
                    categories.push(categoryReference);
                }

                categoryReference.items.push(searchItemsArray[i]);
            }

            // sort categories
            categories.sort(function(a, b) {
                return a.type > b.type;
            });

            var renderData = {
                categories: categories
            };

            this._renderSearchItems(renderData);
        },







        _renderSearchItems: function(renderData) {
            viewRenderer.renderHTML(this._references.$searchItemsContainer, searchCompletionTemplate, renderData);
        },

        _updateSelectedItem: function(offset) {
            var $searchItems = this._references.$searchItemsContainer.find('.js-search-completion-item');

            var $currentActive = $searchItems.filter('.hover');

            var currentIndex = $searchItems.index($currentActive);
            var nextIndex;

            if (currentIndex == -1) {
                if (offset == 1) {
                    nextIndex = 0;
                }
            } else {
                nextIndex = currentIndex + offset;
            }

            nextIndex = Util.Math.mod(nextIndex, $searchItems.length);

            $currentActive.removeClass('hover');
            $searchItems.eq(nextIndex).addClass('hover');

        },

        _selectItem: function() {
            var $currentActive = this._references.$searchItemsContainer.find('.js-search-completion-item.hover');
            var currentURL = $currentActive.attr('href');

            if (!currentURL) {
                return;
            }

            window.location.href = currentURL;
        },

        _onKeyDown: function(e) {
            switch (e.keyCode) {
                // enter
                case 13:
                    e.preventDefault();
                    this._selectItem();
                    break;
                // escape
                case 27:
                    e.preventDefault();
                    this._clearSearchResults();
                    break;
                // up arrow
                case 38:
                    e.preventDefault();
                    this._updateSelectedItem(-1);
                    break;
                // down arrow
                case 40:
                    e.preventDefault();
                    this._updateSelectedItem(1);
                    break;
            }
        },

        _onKeyUp: function(e) {
            switch (e.keyCode) {
                // no need to send extra requests to the server
                // catch these non-changing keys

                // shift
                case 16:
                // control
                case 17:
                // alt
                case 18:
                // insert
                case 45:
                // delete
                case 46:
                // home
                case 36:
                // end
                case 35:
                // page up
                case 33:
                // page down
                case 34:
                // left arrow
                case 37:
                // up arrow
                case 38:
                // right arrow
                case 39:
                // down arrow
                case 40:
                    break;

                default:
                    clearTimeout(this._state.searchInputChangedTimeout);
                    this._state.searchInputChangedTimeout = setTimeout(this._boundFunctions.onSearchInputChangedTimeout, this._config.searchInputChangeRefreshDelay);
                    break;
            }
        },

        _onSearchItemMouseEnter: function(e) {
            this._references.$searchItemsContainer.find('.js-search-completion-item.hover').removeClass('hover');

            var $currentTarget = jQuery(e.currentTarget);
            $currentTarget.addClass('hover');
        },

        _onBodyClick: function(e) {
            this._clearSearchResults();
        },

        _clearSearchResults: function() {
            this._renderSearchItems([]);
        },

        _onSearchInputChangedTimeout: function(){
            var value = this._references.$searchInputBox.val();

            if (value != this.getSearchInputVal()) {
                this.setSearchInputVal(value);
                this._references.dataFeed.clearSearchCompletionCache();

                if (value == "") {
                    this._clearSearchResults();
                } else {
                    this.getSearchItems(value);
                }
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

    return SearchViewController;
});
