define(function(require) {
    'use strict';

    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    
    var BlockDataFeed = DigitalGreenDataFeed.extend({

        constructor: function($language) {
            this.base('api/getblock/');

            // prepare data model
            var blockSubModel = this._dataModel.addSubModel('block', true);
        },

        fetch: function(language) {
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            var dataModel = this._dataModel;
            var blockModel = dataModel.get('block');
            
            blockModel.set('blockObj', unprocessedData.block);
            return unprocessedData.block;
        },

        setInputParam: function(key, value, disableCacheClearing) {
            var paramChanged = this.base(key, value);
            if (paramChanged && !disableCacheClearing) {
                this.clearblockCache();
            }

            return paramChanged;
        },

        clearblockCache: function() {
            this._dataModel.get('block').clear();
        },

        getBlock: function() {
            var blockModel = this._dataModel.get('block');
            var block = blockModel.get('blockObj');

            if (!block) {
                this.fetch();
                return false;
            }
            return block;
        }

    });

    return BlockDataFeed;

});