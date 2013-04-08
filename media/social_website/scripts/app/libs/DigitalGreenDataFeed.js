define(function(require) {
    'use strict';
    
    var DataFeed = require('app/libs/DataFeed');
    var globalEventManager = require('framework/globalEventManager');

    var DigitalGreenDataFeed = DataFeed.extend({

        _boundFunctions: undefined,

        constructor: function(feedURL) {
            this.base(feedURL);

            this.addInputParam('language', false, '', true);
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
            this.setInputParam('language', value);
        },

        _processData: function(unprocessedData) {
            this._state.responseStatus = {
                // data provided by the api
                responseCode: unprocessedData.responseCode,
                requestParameters: unprocessedData.requestParameters,
                errorCode: unprocessedData.errorCode,
                errorDescription: unprocessedData.errorDescription,

                // evaluated measure of success
                success: (unprocessedData.responseCode == 'OK')
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