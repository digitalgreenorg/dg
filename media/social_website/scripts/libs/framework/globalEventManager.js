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

    var globalEventManager = new EventManager();

    return globalEventManager;
});