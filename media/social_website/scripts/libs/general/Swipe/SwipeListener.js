/**
 * SwipeListener Class File
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires EventDrivenObject.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var EventDrivenObject = require('framework/EventManager');
    var jQuery = require('jquery');

    var SwipeListener = EventDrivenObject.extend({

        _managerReference: null,
        _mixedTarget: null,

        /**
         * Configuration Format
         * ----------------------------------------------------------
         * Required:
         * ----------------------------------------------------------
         * swipeType:               swipeManager.SWIPE_TYPES
         * swipeDistance:           integer > 0
         * swipeUnits:              swipeManager.SWIPE_UNITS
         * triggerOnlyOnRelease:    boolean
         * callback:                function
         * ----------------------------------------------------------
         * Optional:
         * ----------------------------------------------------------
         * lockX:                   boolean
         * lockY:                   boolean
         * ----------------------------------------------------------
         */

        _swipeConfigurations: null,

        _state: null,

        constructor: function(managerReference, mixedTarget) {

            this.base();

            this._managerReference = managerReference;
            this._mixedTarget = mixedTarget;

            this._swipeConfigurations = [];

            this._state = {
                swipeActive:            false,
                swipeStartPosition:     null,
                swipePreviousPosition:  null,
                boundSwipeStartEvent:             null,
                axisLocked:             {x: false, y: false}
            };

            this._bindEvents();

        },

        _bindEvents: function() {

            this.addEventListener('swipeStart', this._onSwipeStart.bind(this));
            this.addEventListener('swipeMove', this._onSwipeMove.bind(this));
            this.addEventListener('swipeEnd', this._onSwipeEnd.bind(this));

            var boundSwipeStartEvent = this._state.boundSwipeStartEvent = this.triggerEvent.bind(this, 'swipeStart');
            var mixedTarget = this._mixedTarget;

            // determine type of mixedTarget
            if (mixedTarget instanceof jQuery) {
                // jquery object was provided
                mixedTarget.on(
                    this._managerReference.deviceEvents.startEvent, 
                    boundSwipeStartEvent
                );
            } else if (typeof mixedTarget == 'string') {
                // assume a string selector was provided
                jQuery('body').on(
                    this._managerReference.deviceEvents.startEvent,
                    mixedTarget,
                    boundSwipeStartEvent
                );
            } else {
                throw 'SwipeListener: invalid target provided: ' + mixedTarget;
            }


        },

        addSwipeConfiguration: function(swipeConfiguration) {

            var SWIPE_TYPES = this._managerReference.SWIPE_TYPES;

            switch (swipeConfiguration.swipeType) {
                case SWIPE_TYPES.LEFT:
                case SWIPE_TYPES.RIGHT:
                    this._state.axisLocked.x = true;
                    break;
                case SWIPE_TYPES.UP:
                case SWIPE_TYPES.DOWN:
                    this._state.axisLocked.y = true;
                    break;

                case SWIPE_TYPES.AUTODETECT:
                case SWIPE_TYPES.UP_LEFT:
                case SWIPE_TYPES.DOWN_LEFT:
                case SWIPE_TYPES.UP_RIGHT:
                case SWIPE_TYPES.DOWN_RIGHT:
                    this._state.axisLocked.x = true;
                    this._state.axisLocked.y = true;
                    break;
            }

            this._swipeConfigurations.push(swipeConfiguration);
            return this;
        },

        _getInputPosition: function(e) {

            var returnObj = {
                x: e.originalEvent.touches ? e.originalEvent.touches[0].pageX : e.pageX,
                y: e.originalEvent.touches ? e.originalEvent.touches[0].pageY : e.pageY
            };

            return returnObj;
        },

        _onSwipeStart: function(e) {

            this._state.swipePreviousPosition = this._state.swipeStartPosition = this._getInputPosition(e);
            this._state.swipeActive = true;
        },

        _onSwipeMove: function(e) {

            if (!this._state.swipeActive) {
                return;
            }

            var swipeStartPosition = this._state.swipeStartPosition;
            var swipeCurrentPosition = this._getInputPosition(e);

            for (var i = 0, len = this._swipeConfigurations.length; i < len; i++) {

                var currentSwipeConfiguration = this._swipeConfigurations[i];

                // if not currently swiping, continue
                if (!this._state.swipeActive || currentSwipeConfiguration.triggerOnlyOnRelease) {
                    continue;
                }

                this._examineSwipe(currentSwipeConfiguration, swipeStartPosition, swipeCurrentPosition, e);
            }

            this._state.swipePreviousPosition = swipeCurrentPosition;

        },

        _onSwipeEnd: function(e) {

            if (!this._state.swipeActive) {
                return;
            }

            var swipeStartPosition = this._state.swipeStartPosition;
            var swipePreviousPosition = this._state.swipePreviousPosition;

            for (var i = 0, len = this._swipeConfigurations.length; i < len; i++) {

                var currentSwipeConfiguration = this._swipeConfigurations[i];

                this._examineSwipe(currentSwipeConfiguration, swipeStartPosition, swipePreviousPosition, e);
            }

            this._resetSwipe();
        },

        _resetSwipe: function() {
            this._state.swipeActive = false;
            this._state.swipeStartPosition = null;
            this._state.swipePreviousPosition = null;
        },

        _examineSwipe: function(swipeConfiguration, startPosition, endPosition, e) {

            // calculate distance swiped
            var swipeDistance = this._calculateDistance(startPosition, endPosition);

            // determine if the swipe is long enough to continue
            switch (swipeConfiguration.swipeUnits) {
                case this._managerReference.SWIPE_UNITS.PIXELS:
                    if (swipeDistance < swipeConfiguration.swipeDistance) {
                        // we haven't traveled far enough; exit
                        return;
                    }
                    break;
                // TODO: implement
                case this._managerReference.SWIPE_UNITS.PERCENT:
                    break;
            }

            // by this time, we know we've mached a swipe
            // Disable all other events
            e.preventDefault();
            // detect swipe type
            var swipeType = this._detectDirection(startPosition, endPosition);

            // if a direction was specified with this listener, ensure it matches
            var listenerSwipeType = swipeConfiguration.swipeType;
            if (listenerSwipeType != this._managerReference.SWIPE_TYPES.AUTODETECT && listenerSwipeType != swipeType) {
                return;
            }

            var swipeInformation = {
                distance: swipeDistance,
                type: swipeType
            };

            swipeConfiguration.callback(swipeInformation);
            this._resetSwipe();
        },

        _calculateDistance: function(startPosition, endPosition) {
            var dx = Math.abs(endPosition.x - startPosition.x);
            var dy = Math.abs(endPosition.y - startPosition.y);
            return Math.sqrt((dx * dx) + (dy * dy));
        },

        _detectDirection: function(startPosition, endPosition) {
            var dx = endPosition.x - startPosition.x;
            var dy = endPosition.y - startPosition.y;

            var ratio = null;
            if (dy != 0) {
                ratio = Math.abs(dx / dy);
            } else if (dx != 0) {
                ratio = Math.abs(dy / dx);
            } else {
                // no distance has been traveled
                return false;
            }

            if (
                ratio >= this._managerReference.getConfiguration().diagonalThreshold &&
                ratio <= (1/this._managerReference.getConfiguration().diagonalThreshold)
            ) {
                // swipe was diagonal

                // left
                if (dx < 0) {
                    if (dy < 0) {
                        // up
                        return this._managerReference.SWIPE_TYPES.UP_LEFT;
                    } else {
                        return this._managerReference.SWIPE_TYPES.DOWN_LEFT;
                    }
                } else
                // right
                {
                    if (dy < 0) {
                        // up
                        return this._managerReference.SWIPE_TYPES.UP_RIGHT;
                    } else {
                        return this._managerReference.SWIPE_TYPES.DOWN_RIGHT;
                    }
                }
            } else {
            // swipe was not diagonal
                if (Math.abs(dx) > Math.abs(dy)) {
                    if (dx < 0) {
                        // left
                        return this._managerReference.SWIPE_TYPES.LEFT;
                    } else {
                        // right
                        return this._managerReference.SWIPE_TYPES.RIGHT;
                    }
                } else {
                    // up/down
                    if (dy < 0) {
                        // up
                        return this._managerReference.SWIPE_TYPES.UP;
                    } else {
                        return this._managerReference.SWIPE_TYPES.DOWN;
                    }
                }
            }
        },

        matchTarget: function(mixedTarget, swipeConfiguration) {
            return this._mixedTarget == mixedTarget;
        },

        // TODO: is this still needed?
        matchConfiguration: function(swipeConfiguration) {

            if (
                (swipeConfiguration.swipeType               != null && swipeConfiguration.swipeType                != this._configuration.swipeType) ||
                (swipeConfiguration.swipeAmount             != null && swipeConfiguration.swipeAmount              != this._configuration.swipeAmount) ||
                (swipeConfiguration.swipeUnits              != null && swipeConfiguration.swipeUnits               != this._configuration.swipeUnits) ||
                (swipeConfiguration.triggerOnlyOnRelease    != null && swipeConfiguration.triggerOnlyOnRelease     != this._configuration.triggerOnlyOnRelease) ||
                (swipeConfiguration.callback                != null && swipeConfiguration.callback                 != this._configuration.callback)
            ) {
                return false;
            }

            return true;
        },


        remove: function() {
            this.destructor();
        },

        removeConfiguration: function() {
            // TODO: not yet implemented
        },

        destructor: function() {
            var mixedTarget = this._configuration.mixedTarget;
            var boundSwipeStartEvent = this._state.boundSwipeStartEvent;

            if (mixedTarget instanceof jQuery) {
                // jquery object was provided
                mixedTarget.off(
                    this._managerReference.deviceEvents.startEvent, 
                    boundSwipeStartEvent
                );
            } else if (typeof mixedTarget == 'string') {
                // assume a string selector was provided
                jQuery('body').off(
                    this._managerReference.deviceEvents.startEvent, 
                    mixedTarget,
                    boundSwipeStartEvent
                );
            } else {
                // nothing to do, but no reason to throw as is done in addListener()
            }

            mixedTarget = this._configuration.mixedTarget = null;
            boundSwipeStartEvent = this._state.boundSwipeStartEvent = null;
            this._configuration = null;
            this._managerReference = null;

            this.base();
        }
    });

    return SwipeListener;

});