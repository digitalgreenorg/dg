/**
 * LifecycleBase Class File
 *
 * This class provides a basic structure for memory clean up.
 *
 * @author Ryan DeLuca
 * @version $Id$
 * @requires require.js
 * @requires Base.js
 * @requires jQuery
 */

define([
    'libs/external/Base',
    'jquery'
],
function(
    Base,
    jQuery
) {
    'use strict';

    var LifecycleBase = Base.extend({

        /**
         * @description LifecycleBase constructor
         * @return {object} LifecycleBase
         */
        constructor: function() {
            jQuery(window).on('unload', this._onUnload.bind(this));
            return this;
        },

        /**
         * @description This function is attached to the onunload event of the window, and
         * calls the destructor.
         * @return {void}
         */
        _onUnload: function() {
            this.destroy();
        },

        /**
         * @description LifecycleBase destructor function for all inheriting classes.
         * It is expected that any inheriting classes expand this function
         * to include any clean up code on a per-class basis.  Additionally,
         * this removes the onunload event handler of this object to further
         * clean up the browser memory in the case that the destructor is
         * explicitly called.
         * @return {void}
         */
        destroy: function() {
            jQuery(window).off('unload', this._onUnload.bind(this));
        }
    });

    return LifecycleBase;
});
