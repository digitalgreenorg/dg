/**
 * EventManager Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires LifecycleBase.js
 */

define([
    'framework/LifecycleBase'
],
function(
    LifecycleBase
) {
    'use strict';

    var EventManager = LifecycleBase.extend({

        /**
         * Stored events
         * @type {Object}
         */
        _events: null,

        /**
         * A queue for events to be triggered
         * @type {Object}
         */
        _eventQueue: null,

        /**
         * Whether or not to queue events
         * @type {Boolean}
         */
        _queueingEvents: false,

        /**
         * EventManager public constructor
         * @return {void}
         */
        constructor: function() {
            this._constructor();
        },

        /**
         * EventManager passive constructor
         * @return {void}
         */
        _constructor: function() {
            this._events = {};
            this._eventQueue = [];
        },

        /**
         * A function to check whether or not the EventManager has been constructed.
         * This function will also run the passive constructor if it hasn't previously been run.
         * @return {void}
         */
        _checkConstructed: function() {
            if (this._events === null) {
                this._constructor();
            }
        },

        /**
         * A function to enable or disable event queueing
         * @param {Boolean} val The new queueing state
         * @return {void}
         */
        setEventQueueing: function(val) {
            this._checkConstructed();
            this._queueingEvents = !!val;
        },

        /**
         * Trigger all queued events and flush the queue
         * @return {void}
         */
        triggerFlushQueue: function() {

            this._checkConstructed();

            if (!this._eventQueue.length) {
                return;
            }

            var oldQueueingEventsValue = this._queueingEvents;
            this._queueingEvents = false;

            for (var i = 0, len = this._eventQueue.length; i < len; i++) {
                var currentEvent = this._eventQueue[i];

                var args = currentEvent.args;
                args.unshift(currentEvent.id);

                // this.trigger(this._eventQueue[i]);
                this.trigger.apply(this, args);
            }

            // clear event queue
            this._eventQueue.splice(0);

            this._queueingEvents = oldQueueingEventsValue;
        },

        /**
         * Add new event
         * @param  {String}   eventId The event id to attach the function to
         * @param  {Function} fn      The function to attach
         * @return {EventManager}     this
         */
        on: function(eventId, fn) {

            this._checkConstructed();

            var events = this._events;
            if (eventId in events == false) {
                events[eventId] = [];
            }

            events[eventId].push(fn);

            return this;
        },

        /**
         * Remove previously attached event
         * @param  {String}   eventId The event id to remove
         * @param  {Function} fn      The function to remove
         * @return {Boolean}  Whether or not an event was removed
         */
        off: function(eventId, fn) {

            this._checkConstructed();

            var events = this._events;
            if (eventId in events == false) {
                return false;
            }

            var eventFound = false;
            for (var i = 0, len = events[eventId].length; i < len; i++) {
                if (events[eventId][i] == fn) {
                    eventFound = true;
                    events[eventId].splice(i, 1);
                }
            }

            return eventFound;
        },

        /**
         * Clear all events from the event manager
         * @return {void}
         */
        clearAllEvents: function() {

            this._checkConstructed();

            var events = this._events;
            for (var id in events) {
                events[id] = null;
                delete(events[id]);
            }
        },

        /**
         * Trigger an event by id
         * @param  {String} eventId The event id to trigger
         * @return {Boolean}        An indicator as to whether or not an event was triggered
         */
        trigger: function(eventId) {

            this._checkConstructed();

            var args = Array.prototype.slice.call(arguments, 1);

            if (this._queueingEvents) {
                this._eventQueue.push({
                    id: eventId,
                    args: args
                });
                return;
            }

            var events = this._events;
            if (eventId in events == false || events[eventId].length == 0) {
                return false;
            }

            var eventsToTrigger = events[eventId];
            var eventHasBeenTriggered = false;
            for (var i = 0, len = eventsToTrigger.length; i < len; i++) {
                var eventToTrigger = eventsToTrigger[i];
                if (typeof eventToTrigger != 'function') {
                    continue;
                }

                if (!args.length) {
                    eventsToTrigger[i].call(this);
                } else {
                    eventsToTrigger[i].apply(this, args);
                }

                eventHasBeenTriggered = true;
            }

            return eventHasBeenTriggered;
        },

        /**
         * EventManager destructor
         * @return {void}
         */
        destroy: function() {
            this.clearAllEvents();
            this.base();
        }
    });

    return EventManager;
});