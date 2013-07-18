/**
 * SlideShowController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires LifecycleBase.js
 */

define(function(require) {

    'use strict';

    require('framework/misc/polyfills');
    var LifecycleBase = require('framework/LifecycleBase');

    var Bootstrap = LifecycleBase.extend({

        /**
         * Bootstrap Configuration
         * @type {Object}
         */
        _config: null,

        /**
         * Global Helpers
         * @type {Object}
         */
        _globalHelpers: null,

        /**
         * A flag marking whether or not the root controller has been initialized
         * @type {Boolean}
         */
        _controllerInitialized: false,

        /**
         * Bootstrap constructor
         * @param  {Object} bootstrapConfig Bootstrap configuration
         * @param  {Boolean} autoInit       Whether or not the bootstrap should init automatically
         * @return {Bootstrap}              this
         */
        constructor: function(bootstrapConfig, autoInit) {

            this.base();

            if (bootstrapConfig == null) {
                bootstrapConfig = {};
            }

            this._config = bootstrapConfig;
            this._globalHelpers = {};

            if (autoInit === false) {
                return;
            }
            
            this._initController();

            return this;
        },

        /**
         * A function for registering a global helper
         * @param  {String} name The name to register the helper by
         * @param  {Object} obj  The helper
         * @return {Bootstrap}   this
         */
        registerGlobalHelper: function(name, obj) {
            if (!name || typeof name != 'string' || !obj || typeof obj != 'object') {
                return;
            }

            this._globalHelpers[name] = obj;
            return this;
        },

        /**
         * Public accessor to init the base controller
         * @return {Bootstrap} this
         */
        init: function() {
            this._initController();
            return this;
        },

        /**
         * Function to init the base controller
         * @return {Bootstrap} this
         */
        _initController: function() {
            if (this._controllerInitialized) {
                return;
            }

            var body = document.body;
            var controllerName = body.getAttribute('data-controller');
            
            // if no default controller was found, exit
            if (!controllerName) {
                return;
            }

            // convert first letter to upper case
            controllerName = controllerName.charAt(0).toUpperCase() + controllerName.substr(1);

            var self = this;

            // finally, init the controller
            require(
                [
                    'controllers/' + controllerName + 'Controller'
                ],
                function(currentController) {
                    self._controller = new currentController(self._config, self._globalHelpers);
                }
            );

            this._controllerInitialized = true;
        },

        /**
         * Bootstrap destructor
         * @return {void}
         */
        destroy: function() {
            this._controller = null;

            this.base();
        }

    });

    return Bootstrap;
});