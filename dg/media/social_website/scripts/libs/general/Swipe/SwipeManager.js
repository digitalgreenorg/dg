/**
 * SwipeManager Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires LifeCycleBase.js
 * @requires SwipeListener.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var LifeCycleBase = require('framework/LifecycleBase');
    var SwipeListener = require('libs/general/Swipe/SwipeListener');
    var jQuery = require('jquery');

    var SwipeManager = LifeCycleBase.extend({

        _configuration: {
            diagonalThreshold: 0.5
        },
        
        // enum
        SWIPE_UNITS: {
            PIXELS:     0,
            // TODO: PERCENT not yet implemented
            PERCENT:    1
        },

        SWIPE_TYPES: {
            AUTODETECT: 0,
            LEFT:       1,
            RIGHT:      2,
            UP:         3,
            DOWN:       4,
            UP_LEFT:    5,
            DOWN_LEFT:  6,
            UP_RIGHT:   7,
            DOWN_RIGHT: 8
        },

        // internal use
        deviceEvents: null,

        _state: {
            previousScrollPosition: null,
            hasTouchEvents: false
        },

        _listeners: [],

        constructor: function() {

            this.deviceEvents = {};

            // detect whether the browser has touch events available
            var hasTouchEvents = this._state.hasTouchEvents = 'ontouchend' in document;

            if (hasTouchEvents) {
                this.deviceEvents.startEvent  = 'touchstart';
                this.deviceEvents.moveEvent   = 'touchmove';
                this.deviceEvents.endEvent    = 'touchend';
            } else {
                this.deviceEvents.startEvent  = 'mousedown';
                this.deviceEvents.moveEvent   = 'mousemove';
                this.deviceEvents.endEvent    = 'mouseup';
            }

            this._bindEvents();

            this._state.previousScrollPosition = {
                x: window.scrollX,
                y: window.scrollY
            };
        },

        _bindEvents: function() {

            jQuery('body')
                .on(this.deviceEvents.moveEvent,  this._onSwipeMove.bind(this))
                .on(this.deviceEvents.endEvent,   this._onSwipeEnd.bind(this));

            // NOTE: this code has been deactivated in hopes for a better solution
            // jQuery(window).on('scroll', this._onWindowScroll.bind(this));
        },

        // NOTE: this code has been deactivated in hopes for a better solution
        // _onWindowScroll: function() {
        //     this.updateScrollPosition();
        // },

        // updateScrollPosition: function() {
        //     this._state.previousScrollPosition.x = window.scrollX;
        //     this._state.previousScrollPosition.y = window.scrollY;
        // },

        getConfiguration: function() {
            return this._configuration;
        },

        /**
         * Add a swipe listener to the manager
         *
         * @param mixed mixedListener Can be an instance of SwipeListener, or a mixed target [jQuery object | string] to create a listener from
         * 
         * @returns SwipeListener
         */
        addListener: function(mixedListener) {

            var listenerToAdd = null;

            if (mixedListener instanceof SwipeListener) {
                // TODO: check if an existing listener exists with the same target
                // if so, merge the configurations and don't add the listener
                // this will prevent multiple listeners with the same target
                // and alleviate the need for removeListener() to continue looping
                // after finding a match

                // mixedListener is already a SwipeListener object
                listenerToAdd = mixedListener;
            } else {
                // mixedListener is not a SwipeListener object

                // check if we already have a listener
                listenerToAdd = this.getListenerByTarget(mixedListener);

                // if the listener already exists within the manager, simply return it
                if (listenerToAdd) {
                    return listenerToAdd;
                }

                // the listener didn't exist within the manager, create a new listener
                listenerToAdd = new SwipeListener(this, mixedListener);
            }

            // add the listener to the manager
            this._listeners.push(listenerToAdd);

            // return the listener
            return listenerToAdd;

        },

        _getListenerIndex: function(mixedTarget) {
            for (var i = 0, len = this._listeners.length; i < len; i++) {
                if (this._listeners[i].matchTarget(mixedTarget)) {
                    return i;
                }
            }

            return false;
        },

        _getListenerByIndex: function(index) {
            var listeners = this._listeners;

            if (listeners.length == 0 || index < 0 || index >= listeners.length) {
                return false;
            }

            return this._listeners[index];
        },

        getListenerByTarget: function(mixedTarget) {
            return this._getListenerByIndex(this._getListenerIndex(mixedTarget));
        },

        removeListener: function(mixedTarget) {
            var listenerIndex = null;
            while (false !== (listenerIndex = this._getListenerIndex(mixedTarget))) {
                var listenerToRemove = this._getListenerByIndex[listenerIndex];
                if (listenerToRemove) {
                    currentListener.remove();
                    this._listeners.splice(listenerIndex, 1);
                }
            }
        },

        removeAllListeners: function() {
            for (var i = 0, len = this._listeners.length; i < len; i++) {
                this._listeners[i].remove();
            }

            this._listeners.splice(0);
        },

        removeSwipeConfiguration: function(mixedTarget, swipeConfiguration) {
            var listener = this.getListenerByTarget(mixedTarget);

        },

        _onSwipeMove: function(e) {
            for (var i = 0, len = this._listeners.length; i < len; i++) {
                this._listeners[i].triggerEvent('swipeMove', e);
            }
        },

        _onSwipeEnd: function(e) {
            for (var i = 0, len = this._listeners.length; i < len; i++) {
                this._listeners[i].triggerEvent('swipeEnd', e);
            }
        },


        _reverseEnum: function(obj, value) {
            for (var key in obj) {
                if (obj[key] == value) {
                    return key;
                }
            }

            return null;
        },

        destructor: function() {
            this.removeAllListeners();

            // TODO: event unbinding (body, window)

            this.base();

        }
    });

    return SwipeManager;
});
