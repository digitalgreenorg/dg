/**
 * Controller Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires EventManager.js
 */

define(function(require) {
    'use strict';

    var EventManager = require('framework/EventManager');

    var Controller = EventManager.extend({

        /**
         * An object to store configuration data
         * @type {Object}
         */
        _config: undefined,

        /**
         * An object cache of references
         * @type {Object}
         */
        _references: null,

        /**
         * An object cache of bound functions
         * @type {Object}
         */
        _boundFunctions: null,

        /**
         * An object cache of state related variables
         * @type {Object}
         */
        _state: undefined,

        /**
         * App Controller Constructor
         * @param  {Object} bootstrapConfig Configuration from the bootstrap
         * @return {Controller} this
         */
        constructor: function($referenceBase, params) {
            this.base();

            if (params == undefined) {
                params = {};
            }

            // init config
            this._config = this._config || {};
            this._initConfig(params);

            // set references
            this._references = this._references || {};
            this._initReferences($referenceBase, params);

            // init events
            this._boundFunctions = this._boundFunctions || {};
            this._initEvents(params);

            //init state
            this._state = this._state || {};
            this._initState(params);

            return this;
        },

        /**
         * Function to organize config init
         * @return {void}
         */
        _initConfig: function(params) {},

        /**
         * Function to organize reference init
         * @return {void}
         */
        _initReferences: function($referenceBase, params) {},

        /**
         * Function to organize event binding functionality
         * @return {void}
         */
        _initEvents: function(params) {},

        /**
         * Function to organize state init
         * @return {void}
         */
        _initState: function(params) {},

        /**
         * App Controller destructor
         * @return {void}
         */
        destroy: function() {
            this._config = undefined;
            this._references = undefined;

            // TODO: loop through and detach events?
            this._boundFunctions = undefined;

            this._state = undefined;

            this.base();
        }
    });

    return Controller;
});