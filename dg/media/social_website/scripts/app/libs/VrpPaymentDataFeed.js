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
    
    var VrpPaymentDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/getReport/');

            // prepare data model
            var vrppaymentSubModel = this._dataModel.addSubModel('vrppayment', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var vrppaymentModel = dataModel.get('vrppayment');
            
            vrppaymentModel.set('vrppaymentObj', unprocessedData.vrppayment);
            return unprocessedData.vrppayment;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearvrppaymentCache();
            }

            return paramChanged;
        },

        clearvrppaymentCache: function() {
            this._dataModel.get('vrppayment').clear();
        },

        getReport: function() {
            var vrppaymentModel = this._dataModel.get('vrppayment');
            var vrppayment = vrppaymentModel.get('vrppaymentObj');

            if (!vrppayment) {
                this.fetch();
                return false;
            }
            return vrppayment;
        }

    });

    return VrpPaymentDataFeed;

});