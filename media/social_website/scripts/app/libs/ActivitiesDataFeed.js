define(function(require) {
    'use strict';
    
    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');

    var ActivitiesDataFeed = DigitalGreenDataFeed.extend({

        _filters: undefined,

        /*
        Input params:

        One of:
        partnerUID {String}
        farmerID {String}
        userUID {String}

        page {Number}
        count {Number}

        Output params:
        collections {Collection[]}
        totalCount {Number}
        */

        constructor: function() {
            this.base('api/activity/');

            // prepare data model
            var activitiesSubModel = this._dataModel.addSubModel('activities', true);

            this.addInputParam('partnerUID', false, undefined, true, activitiesSubModel);
            this.addInputParam('farmerID', false, undefined, true, activitiesSubModel);
            this.addInputParam('userUID', false, undefined, true, activitiesSubModel);
            this.addInputParamCacheClear('language__name', activitiesSubModel);

            this.addInputParam('offset', false);
            this.addInputParam('limit', false);
        },

        fetch: function(page, countPerPage) {
            if (page == undefined) {
                page = 0;
            }

            if (countPerPage == undefined) {
                countPerPage = 5;
            }

            this.setInputParam('offset', page, true);
            this.setInputParam('limit', countPerPage, true);

            // perform the fetch
            this.base();
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);
            
            // local references
            var dataModel = this._dataModel;
            var model = dataModel.get('activities');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.meta.limit;
            var page = unprocessedData.meta.offset;

            // store total count
            dataModel.set('totalCount', unprocessedData.meta.total_count);
            // import
            var dataToAdd = unprocessedData.activities;
            var startingCacheId = page * countPerPage;

            model.addSubset(dataToAdd, startingCacheId);
        },

        clearCollectionCache: function() {
            this._dataModel.get('activities').clear();
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        getActivities: function() {

            var page = this.getInputParam('offset');
            var countPerPage = this.getInputParam('limit');

            var data = this._dataModel.get('activities').getSubset(page * countPerPage, countPerPage);

            if (!data) {
                this.fetch(page, countPerPage);
                return false;
            }

            return data;
        }

    });

    return ActivitiesDataFeed;

});