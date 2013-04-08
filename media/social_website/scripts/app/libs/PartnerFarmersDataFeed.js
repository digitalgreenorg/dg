define(function(require) {
    'use strict';
    
    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');

    var PartnerFarmersDataFeed = DigitalGreenDataFeed.extend({

        _filters: undefined,

        /*
        Input params:

        One of:
        partnerUID {String}

        page {Number}
        count {Number}

        Output params:
        farmers {Farmer[]}
        totalCount {Number}
        */

        constructor: function() {
            this.base('api/partnerFarmers.php');

            // prepare data model
            var partnerFarmersSubModel = this._dataModel.addSubModel('partnerFarmers', true);

            this.addInputParam('partnerUID', false, undefined, true, partnerFarmersSubModel);
            this.addInputParamCacheClear('language', partnerFarmersSubModel);

            this.addInputParam('page', false);
            this.addInputParam('count', false);

            this.getPartnerFarmers();
        },

        fetch: function(page, countPerPage) {
            if (page == undefined) {
                page = 0;
            }

            if (countPerPage == undefined) {
                countPerPage = 12;
            }

            this.setInputParam('page', page, true);
            this.setInputParam('count', countPerPage, true);

            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var model = dataModel.get('partnerFarmers');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.requestParameters.count;
            var page = unprocessedData.requestParameters.page;

            // store total count
            dataModel.set('totalCount', unprocessedData.totalCount);

            // import
            var dataToAdd = unprocessedData.farmers;
            var startingCacheId = page * countPerPage;

            model.addSubset(dataToAdd, startingCacheId);
        },

        clearCollectionCache: function() {
            this._dataModel.get('partnerFarmers').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getPartnerFarmers: function() {

            var page = this.getInputParam('page');
            var countPerPage = this.getInputParam('count');

            var data = this._dataModel.get('partnerFarmers').getSubset(page * countPerPage, countPerPage);

            if (!data) {
                this.fetch(page, countPerPage);
                return false;
            }

            return data;
        }

    });

    return PartnerFarmersDataFeed;

});