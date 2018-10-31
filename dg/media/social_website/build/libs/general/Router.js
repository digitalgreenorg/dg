/**
 * Router Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 */

define(function() {
    'use strict';

    /**
     * Router constructor
     * @param {String} delimiter    The delimiter used to separate/parse route pieces
     * @param {Function} broadcast  A broadcast function callback to add on construct
     * @return {void}
     */
    var Router = function(delimiter, broadcast) {

        this._delimiter = delimiter || '/';
        this._externalBroadcastFunctions = [];
        this._broadcastArgs = null;

        this.addBroadcast(broadcast);

        var w = window;
        if (w.addEventListener) {
            w.addEventListener('hashchange', this._onHashChange.bind(this));
        } else {
            w.attachEvent('onhashchange', this._onHashChange.bind(this));
        }

        this.broadcast();
    };

    /**
     * Add a broadcast function callback
     * @param {Function} fn The callback to add
     * @return {Router} this
     */
    Router.prototype.addBroadcast = function(fn) {
        if (fn && typeof fn == 'function') {
            this._externalBroadcastFunctions.push(fn);
        }

        return this;
    };

    /**
     * Remove a broadcast function callback
     * @param  {Function} fn The callback to remove
     * @return {Router}   this
     */
    Router.prototype.removeBroadcast = function(fn) {
        // TODO: this function needs to be tested
        var i = 0;
        var len = this._externalBroadcastFunctions.length;

        for (; i < len; i++) {
            if (this._externalBroadcastFunctions[i] == fn) {
                this._externalBroadcastFunctions.splice(i, 1);
            }
        }

        return this;
    };

    /**
     * Event fired when the browser's hash tag changes
     * @return {void}
     */
    Router.prototype._onHashChange = function() {
        this.broadcast();
    };

    /**
     * Initiate the broadcasting of new route information to all listener functions
     * @param  {Object} broadcastArgs Additional arguments to pass to broadcast callbacks
     * @return {Router}               this
     */
    Router.prototype.broadcast = function(broadcastArgs) {

        // use directly passed in broadcast args if present
        // othereise, fall back to those that may be present at object level
        broadcastArgs = broadcastArgs || this._broadcastArgs;
        this._broadcastArgs = null;

        var hash = window.location.hash;
        hash = this._stripLeadingCharacters(hash);

        var route = (hash == '')
            ? []
            : hash.split(this._delimiter + '');
        
        this._callBroadcastFunctions(route, broadcastArgs);

        return this;
    };

    /**
     * Cycle through and trigger all broadcast callbacks
     * @param  {Array} route         Route information
     * @param  {Object} broadcastArgs Additional arguments to pass to the broadcast callbacks
     * @return {void}
     */
    Router.prototype._callBroadcastFunctions = function(route, broadcastArgs) {
        var broadcast = this._externalBroadcastFunctions;
        var len = broadcast.length;

        if (len == 0) {
            return;
        }

        var i = 0;
        for (; i < len; i++) {
            broadcast[i](route, broadcastArgs);
        }
    };

    /**
     * Helper function to strip empty delimited pieces from the route hash
     * @param  {String} hash Input hash string
     * @return {String}      Cleaned up hash string
     */
    Router.prototype._stripLeadingCharacters = function(hash) {
        var r = new RegExp('^#(' + this._delimiter + ')*');
        return hash.replace(r, '');
    };

    /**
     * Trigger the changing of the browser hash, which will subsequently trigger the onHashChange event
     * @param  {Array|String} mixedHash     Input hash data
     * @param  {Object} broadcastArgs Additional arguments to pass to the broadcast callbacks
     * @return {void}
     */
    Router.prototype.go = function(mixedHash, broadcastArgs) {
        if (mixedHash instanceof Array) {
            mixedHash = mixedHash.join(this._delimiter);
        }

        if (typeof mixedHash != 'string') {
            throw 'Router.go(): invalid location provided.';
        }

        mixedHash = this._stripLeadingCharacters(mixedHash);

        this._broadcastArgs = broadcastArgs;

        window.location.hash = '#' + this._delimiter + mixedHash;
    };

    return Router;
});