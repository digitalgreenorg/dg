/**
 * PracticeMappingDataFeed Class File
 *
 * @author aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    
    var DeoDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/getdeo/');

            // prepare data model
            var deoSubModel = this._dataModel.addSubModel('deo', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var deoModel = dataModel.get('deo');
            
            deoModel.set('deoObj', unprocessedData.deo);
            return unprocessedData.deo;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.cleardeoCache();
            }

            return paramChanged;
        },

        cleardeoCache: function() {
            this._dataModel.get('deo').clear();
        },

        getDeo: function() {
            var deoModel = this._dataModel.get('deo');
            var deo = deoModel.get('deoObj');

            if (!deo) {
                this.fetch();
                return false;
            }
            return deo;
        }

    });

    return DeoDataFeed;

});