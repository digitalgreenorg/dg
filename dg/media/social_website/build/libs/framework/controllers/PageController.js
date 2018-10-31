/**
 * PageController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires Controller.js
 */

define(function(require) {
    'use strict';

    var Controller = require('framework/controllers/Controller');
    var jQuery = require('jquery');

    var PageController = Controller.extend({

        /**
         * Configuration from the bootstrap
         * @type {Object}
         */
        _bootstrapConfig: null,

        /**
         * Information about the user's browser
         * @type {Object}
         */
        _browserInformation: null,

        /**
         * Information regarding the size of the window
         * @type {Object}
         */
        _windowSize: null,

        /**
         * The current size range as provided by the bootstrap
         * @type {Object}
         */
        _currentSizeRange: null,

        /**
         * Global helpers
         * @type {Object}
         * @static
         */
        _globalHelpers: {},

        /**
         * App Controller Constructor
         * @param  {Object} bootstrapConfig Configuration from the bootstrap
         * @return {PageController} this
         */
        constructor: function(bootstrapConfig, globalHelpers, $referenceBase) {
            this.base($referenceBase);

            bootstrapConfig || (bootstrapConfig = {});
            this._bootstrapConfig = bootstrapConfig;

            this.setGlobalHelpers(globalHelpers);

            // some events or other functionality may need browser information when firing
            this.__detectBrowser();

            // do initial setting of window size and size range
            this.__updateWindowSize();
            this.__updateSizeRange();

            return this;
        },

        /**
         * Function to set the global helper reference
         * @param {Object} helpers Reference to a global helper object
         * @return {PageController} this
         */
        setGlobalHelpers: function(helpers) {
            var id;
            for (id in helpers) {
                this.globalHelper(id, helpers[id]);
            }

            return this;
        },
        
        /**
         * Setter/getter for for global helpers
         * @param  {String} name   The name by which to store the global helper
         * @param  {Object} helper The global helper
         * @return {void}
         */
        globalHelper: function(name, helper) {

            if (! name || typeof name != 'string') {
                return;
            }

            if (helper == null) {
                return this._globalHelpers[name];
            }

            this._globalHelpers[name] = helper;
        },

        /**
         * Getter for browser information
         * @return {Object} Browser information object
         */
        getBrowserInformation: function() {
            return this._browserInformation;
        },

        /**
         * Getter for the mobile status of the user
         * @return {Boolean} Whether or not the user is on a mobile platform
         */
        isMobile: function() {
            return this._browserInformation.isMobile;
        },

        /**
         * A function stub that gets called when the user's browser size range changes
         * @return {void}
         */
        _onSizeRangeChange: function() {},

        /**
         * App Controller destructor
         * @return {void}
         */
        destroy: function() {
            this._bootstrapConfig = null;
            this._bootstrapData = null;

            this.base();
        },



        /**
         * The following functions are meant for internal use,
         * and are not meant to be extended
         */

        /**
         * Function to gather information about the user's browser
         * @return {void}
         */
        __detectBrowser: function() {
            var navigatorAgent = navigator.userAgent.toLowerCase();

            var isiPhone = navigatorAgent.indexOf('iphone');
            var isiPad = navigatorAgent.indexOf('ipad');
            var isiPod = navigatorAgent.indexOf('ipod');

            var isIOS =  (isiPhone > -1 ||
                isiPad > -1 ||
                isiPod > -1);

            var isAndroid = navigatorAgent.indexOf('android') > -1;

            var isIE = jQuery.browser.msie == true;
            var IEVersion = (isIE)
                ? parseFloat(jQuery.browser.version, 10)
                : undefined;

            var browserInformation = this._browserInformation = {
                isIE: isIE,
                IEVersion: IEVersion,
                isIOS: isIOS,
                isAndroid: isAndroid,
                isMobile: isIOS || isAndroid,
                hasTouchEvents: (('ontouchstart' in window) || window.DocumentTouch && document instanceof DocumentTouch)
            }

            // add a mobile class to the body for mobile devices
            var body = document.body;
            if (browserInformation.isMobile) {
                body.className += ((body.className != '') ? ' ' : '') + 'mobile';
            }
        },

        /**
         * Callback for window resize event
         * @return {void}
         */
        __onWindowResize: function() {
            this.__updateWindowSize();
        },

        /**
         * Function to update internal data and fire events
         * @return {void}
         */
        __updateWindowSize: function() {
            var oldWindowSize = this._windowSize;
            this.__readWindowSize();
            var newWindowSize = this._windowSize;

            // if we have a previous window size, and the size hasn't changed, exit
            if (oldWindowSize != null && oldWindowSize.width == newWindowSize.width && oldWindowSize.height == newWindowSize.height) {
                return;
            }

            this.trigger('windowResized');

            this.__updateSizeRange();
        },

        /**
         * Function to update internal size range data
         * @return {void}
         */
        __updateSizeRange: function() {

            var windowSize = this._windowSize;

            // determine if the size range changed
            var previousSizeRange = this._currentSizeRange;

            var sizeRanges = this._bootstrapConfig.sizeRanges;
            if (!(sizeRanges && sizeRanges instanceof Array)) {
                return;
            }

            for (var i = 0, len = sizeRanges.length; i < len; i++) {
                var currentSizeRange = sizeRanges[i];

                if (
                    windowSize.width > currentSizeRange.minWidth && 
                    (
                        currentSizeRange.maxWidth == null || 
                        windowSize.width <= currentSizeRange.maxWidth
                    )
                ) {
                    this._currentSizeRange = currentSizeRange;

                    if (previousSizeRange != currentSizeRange) {
                        this.triggerEvent('sizeRangeChanged', currentSizeRange);
                    }

                    break;
                }
            }
        },

        /**
         * Function to gather window size
         * @return {void}
         */
        __readWindowSize: function() {
            var $window = jQuery(window);

            this._windowSize = {
                width: $window.width(),
                height: $window.height()
            }
        }
    });

    return PageController;
});