define(function(require) {
    'use strict';
    
    var DataFeed = require('app/libs/DataFeed');
    var globalEventManager = require('framework/globalEventManager');
    var appConfig = require('appConfig');
    
    var DigitalGreenDataFeed = DataFeed.extend({

        _boundFunctions: undefined,

        constructor: function(feedURL) {
            this.base(appConfig.apiUrl + feedURL);
            
            this.addInputParam('language__name', false, '', true);
        },

        _initConfig: function() {
            this.base();
            this._config.fetchDelay = 500;
        },

        // TODO: if desired, implement functionality to read/store/etc. 
        // results from the API common to all API calls
        // Currently we have no need for them

        // responseCode
        // requestParameters
        // errorCode
        // errorDescription

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;

            boundFunctions.onLanguageChanged = this._onLanguageChanged.bind(this);
            globalEventManager.on('languageChanged', boundFunctions.onLanguageChanged);
        },

        _onLanguageChanged: function(value) {
            this.setInputParam('language__name', value);
        },

        _processData: function(unprocessedData) {
        	var success= false;
        	// following if loops are to find out whether success is true or false
        	// success should be true when (1)user clicks LIKE or (2)the user/video query is present id DB
        	if (unprocessedData != undefined){
        		if (unprocessedData.id != undefined){
        			success = true;
        		}
        		else if (unprocessedData.objects.length > 0){
        			success = true;
        		}
        	}
            this._state.responseStatus = {
                // data provided by the api
                responseCode: unprocessedData.responseCode,
                requestParameters: unprocessedData.requestParameters,
                errorCode: unprocessedData.errorCode,
                errorDescription: unprocessedData.errorDescription,
                success: success
            };

            // ENHANCEMENT: upon a response code of "ERROR", implement
            // auto-retry functionality that will retry up to N times?
        },

        getResponseStatus: function() {
            return this._state.responseStatus;
        },

        destroy: function() {
            this.base();
        }

    });

    return DigitalGreenDataFeed;

});