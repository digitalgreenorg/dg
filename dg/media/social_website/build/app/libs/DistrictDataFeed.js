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
    
    var DistrictDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/getdistrict/');

            // prepare data model
            var districtSubModel = this._dataModel.addSubModel('district', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var districtModel = dataModel.get('district');
            
            districtModel.set('districtObj', unprocessedData.district);
            return unprocessedData.district;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.cleardistrictCache();
            }

            return paramChanged;
        },

        cleardistrictCache: function() {
            this._dataModel.get('district').clear();
        },

        getDistrict: function() {
            var districtModel = this._dataModel.get('district');
            var district = districtModel.get('districtObj');

            if (!district) {
                this.fetch();
                return false;
            }
            return district;
        }

    });

    return DistrictDataFeed;

});