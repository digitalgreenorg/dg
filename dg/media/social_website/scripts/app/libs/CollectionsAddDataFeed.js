/**
 * CollectionsAddDataFeed Class File
 *
 * @author Aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */
define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    var Util = require('framework/Util');

    var CollectionAddDataFeed = DigitalGreenDataFeed.extend({

        constructor: function() {
            this.base('api/collections/');

            this._dataModel.addSubModel('objects', true);
        },

        fetch: function(customCallback) {
            
            this.base(null, customCallback);
        },

        _onFetchError: function(error) {
            this.base(error);
            if(error.status == 400){
                $('body').scrollTop(0);
                $(".coltitle").notify(error.responseText);
            }
        },
        
        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            return unprocessedData;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearCache();
            }

            return paramChanged;
        },

        clearCache: function() {
            this._dataModel.get('objects').clear();
        },


    });

    return CollectionAddDataFeed;

});