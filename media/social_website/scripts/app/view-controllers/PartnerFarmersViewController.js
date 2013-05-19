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

    var PartnerFarmersDataFeed = require('app/libs/PartnerFarmersDataFeed');
    var partnerFarmerTemplate = require('text!app/views/partnerFarmer.html');

    var PartnerFarmersViewController = Controller.extend({

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

            references.dataFeed = new PartnerFarmersDataFeed();

            references.$farmerCarouselContainer = $referenceBase;
            references.$farmerPagesContainer = $referenceBase.find(".js-partner-farmers-pages-container");
            references.$prevFarmerPageInput = $referenceBase.find(".js-prev-partner-farmers-page");
            references.$nextFarmerPageInput = $referenceBase.find(".js-next-partner-farmers-page");
        },

        _initState: function() {
            this.base();

            var state = this._state;
            state.currentPageNumber = 0;
            state.farmersPerPage = 12;
            state.currentCount = 0;
            state.totalCount = 0;
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);

            // handle paging clicks
            // previons
            boundFunctions.onCarouselPagingPreviousClick = this._onCarouselPagingClick.bind(this, -1);
            references.$prevFarmerPageInput.click(boundFunctions.onCarouselPagingPreviousClick);

            // next
            boundFunctions.onCarouselPagingNextClick = this._onCarouselPagingClick.bind(this, 1);
            references.$nextFarmerPageInput.click(boundFunctions.onCarouselPagingNextClick);
        },

        setCurrentPageNumber: function(n) {
            this._state.currentPageNumber = n;
            return this;
        },

        getCurrentPageNumber: function(){
            return this._state.currentPageNumber;
        },

        setFarmersPerPage: function(value){
            this._state.farmersPerPage = value;
            return this;
        },

        getFarmersPerPage: function(){
            return this._state.farmersPerPage;
        },

        addToCurrentCount: function(n) {
            this._state.currentCount += n;
            return this;
        },

        getTotalPages: function(){
            return Math.ceil(this.getTotalCount()/this.getFarmersPerPage());
        },

        setTotalCount: function(n) {
            this._state.totalCount = n;
            return this;
        },

        getTotalCount: function(){
            return this._state.totalCount;
        },

        getPartnerFarmers: function(page, farmersPerPage) {
            if (page == undefined) {
                page = this.getCurrentPageNumber();
            } else {
                this.setCurrentPageNumber(page);
            }

            if (farmersPerPage == undefined) {
                farmersPerPage = this.getFarmersPerPage();
            } else {
                this.setFarmersPerPage(farmersPerPage);
            }
            
            var dataFeed = this._references.dataFeed;
            dataFeed.setInputParam('offset', page, true)
            dataFeed.setInputParam('limit', farmersPerPage, true);


            var partnerFarmersArray = dataFeed.getPartnerFarmers();
            var totalCount = dataFeed.getTotalCount();

            if(partnerFarmersArray == false){
                return false;
            }

            this._updateFarmersDisplay(partnerFarmersArray, totalCount);
        },

        _onDataProcessed: function() {
            this.getPartnerFarmers();
        },

        _updateFarmersDisplay: function(partnerFarmersArray, totalCount) {
            this._renderPartnerFarmers(partnerFarmersArray);

            this.setTotalCount(totalCount);
            this.addToCurrentCount(partnerFarmersArray.length);
            this.updatePartnerFarmersPaginationDisplay();
        },

        _renderPartnerFarmers: function(partnerFarmersArray) {
            var partnerFarmersRenderArray = [];

            var i = 0;
            var len = partnerFarmersArray.length;
            for (; i < len; i++) {
                var currentPartnerFarmerData = Util.Object.clone(partnerFarmersArray[i], true);
                partnerFarmersRenderArray.push(currentPartnerFarmerData);
            }

            this._references.$farmerPagesContainer.empty();

            var renderData = {
                farmers: partnerFarmersArray
            };

            viewRenderer.renderAppend(this._references.$farmerPagesContainer, partnerFarmerTemplate, renderData);
        },


        updatePartnerFarmersPaginationDisplay: function(){
            //update prev button
            if (this.getCurrentPageNumber() <= 0) {
                this._references.$prevFarmerPageInput.hide();
            } else {
                this._references.$prevFarmerPageInput.show();
            }

            //update next button
            if (this.getCurrentPageNumber() >= this.getTotalPages()) {
                this._references.$nextFarmerPageInput.hide();
            } else {
                this._references.$nextFarmerPageInput.show();

            }
        },

        _onCarouselPagingClick: function(offset, event){
            event.preventDefault();
            event.stopPropagation();

            this.getPartnerFarmers(this.getCurrentPageNumber() + offset);
        },

        setInputParam: function(key, value, disableCacheClearing) {
            this._references.dataFeed.setInputParam(key, value, disableCacheClearing);
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

    return PartnerFarmersViewController;
});
