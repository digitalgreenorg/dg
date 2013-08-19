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
            this.base('api/partnerFarmers/');

            // prepare data model
            var partnerFarmersSubModel = this._dataModel.addSubModel('partnerFarmers', true);

            this.addInputParam('uid', false, undefined, true, partnerFarmersSubModel);
            this.addInputParamCacheClear('language__name', partnerFarmersSubModel);

            this.addInputParam('offset', false);
            this.addInputParam('limit', false);

            this.getPartnerFarmers();
        },

        fetch: function(page, countPerPage) {
            if (page == undefined) {
                page = 0;
            }

            if (countPerPage == undefined) {
                countPerPage = 12;
            }
            this.setInputParam('uid',$(".js-partner-farmers-pages-container").attr('data-partnerID'));
            this.setInputParam('offset', page, true);
            this.setInputParam('limit', countPerPage, true);

            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var model = dataModel.get('partnerFarmers');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.meta.limit;
            var page = unprocessedData.meta.offset;

            // store total count
            dataModel.set('totalCount', unprocessedData.objects[0]['farmer'].length);
            if (dataModel._data.totalCount == 0) {
            	$('.js-partner-farmers-carousel-container').hide();
            }

            // import
            var dataToAdd = unprocessedData.objects[0]['farmer'];
            var startingCacheId = page * countPerPage;

            model.addSubset(dataToAdd, startingCacheId);
            return dataToAdd;
        },

        clearCollectionCache: function() {
            this._dataModel.get('partnerFarmers').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getPartnerFarmers: function() {

            var page = this.getInputParam('offset');
            var countPerPage = this.getInputParam('limit');

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