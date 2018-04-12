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
    
    var PracticeMappingDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/mapping/');

            // prepare data model
            var practiceMappingSubModel = this._dataModel.addSubModel('practiceMapping', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var practiceMappingModel = dataModel.get('practiceMapping');
            
            practiceMappingModel.set('practiceMappingObj', unprocessedData.mapping_dropdown);
            return unprocessedData.mapping_dropdown;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearCollectionDropDownCache();
            }

            return paramChanged;
        },

        clearPracticeMappingCache: function() {
            this._dataModel.get('practiceMapping').clear();
        },

        getPracticeMapping: function() {
            var practiceMappingModel = this._dataModel.get('practiceMapping');
            var practiceMapping = practiceMappingModel.get('practiceMappingObj');

            if (!practiceMapping) {
                this.fetch();
                return false;
            }
            return practiceMapping;
        }

    });

    return PracticeMappingDataFeed;

});