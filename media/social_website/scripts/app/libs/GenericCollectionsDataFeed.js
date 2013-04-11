define(function(require) {
    'use strict';
    
    var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
    var DataModel = require('app/libs/DataModel');
    var Util = require('framework/Util');

    var GenericCollectionsDataFeed = DigitalGreenDataFeed.extend({

        _filters: undefined,

        /*
        Input params:

        page {Number}
        count {Number}
        relativeUserId {string} (optional) -- is this still needed?

        Output params:
        collections {Collection[]}
        totalCount {Number}
        */

        constructor: function(feedURL) {
            this.base(feedURL);

            var dataModel = this._dataModel;

            // prepare data model
            var collectionsSubModel = dataModel.addSubModel('collections', true);

            // set up input params
            this.addInputParam('offset', true, 0, true);
            // TODO: if count per page could *ever* be changed by the user, additional
            // work would need to be done to either invalidate the last group of entries
            // of any newly created "partial" pages, invalidate the whole cache, etc.
            // to ensure collections are cached properly (ex: getsubset is called on the
            // model, we haven't reached our total count yet (there are more entries after,
            // this page) the first entry of the page is not undefined, so it considers 
            // that page valid, but some entries later on are undefined)
            // This TODO applies to all places where paging is present and the count may change.
            // Alternatively, we could verify all entries in the subset range are NOT
            // undefined to decide whether a page is valid; if this is done, we need to
            // implement functionality for allowing partial page retrieval for the last
            // page in a set since each page (m) may not have a number of total entries
            // equal to n * m
            this.addInputParam('count', true, 10, true);
        },

        _processData: function(unprocessedData) {
            this.base(unprocessedData);

            // local references
            var dataModel = this._dataModel;
            var collectionsModel = dataModel.get('collections');

            // gather count and page for caching and saving purposes
            var countPerPage = unprocessedData.requestParameters.limit;
            var page = unprocessedData.requestParameters.offset;

            // store total count
            dataModel.set('totalCount', unprocessedData.totalCount);

            // import collections from data
            var collectionsToAdd = unprocessedData.collections;
            var startingCacheId = page * countPerPage;

            collectionsModel.addSubset(collectionsToAdd, startingCacheId);
        },

        getTotalCount: function() {
            return this._dataModel.get('totalCount');
        },

        checkHaveAllCollections: function() {
            var collectionsStored = this._dataModel.get('collections').get().length;
            var totalCount = this.getTotalCount();

            var haveAllCollections = (collectionsStored >= totalCount);

            if (haveAllCollections) {
                var totalCount = this.getTotalCount();

                this.trigger('totalNumberOfCollectionsReached', {
                    currentPage: this.getInputParam('offset'),
                    totalPages: Math.ceil(totalCount / this.getInputParam('limit')),
                    totalCount: totalCount
                });
            }

            return haveAllCollections;
        },

        _translatePageDescriptor: function(pageDescriptor) {
            var pageNumber = this.getInputParam('offset');

            if (pageDescriptor != undefined) {
                switch (pageDescriptor) {
                    case 'next':
                        pageNumber++;
                        break;
                    case 'previous':
                        if (--pageNumber < 0) {
                            pageNumber = 0;
                        }
                        break;
                    case 'first':
                        pageNumber = 0;
                        break;
                    default:
                        pageNumber = parseInt(pageDescriptor, 10);
                        break;
                }

            }

            return pageNumber;
        },

        setCollectionsPage: function(pageDescriptor) {
            var pageNumber = this._translatePageDescriptor(pageDescriptor);

            this.setInputParam('offset', pageNumber);

            return pageNumber;
        },

        getCollectionsPage: function(pageDescriptor, overrideData, onHaveCollectionsCallback) {

            this.setCollectionsPage(pageDescriptor);

            var countPerPage = this.getInputParam('limit');

            var collectionsModel = this._dataModel.get('collections');

            // determine if we've retrieved all collections
            var collectionsStored = collectionsModel.get().length;

            // attempt to retrieve the desired subset
            // if we don't currently have the desired subset, attempt to retrieve it
            if (!collectionsModel.hasSubset(pageDescriptor * countPerPage, countPerPage)) {
                // if we've not yet received all collections possible, get more
                if (!this.checkHaveAllCollections()) {
                    var returnCallback = this._onCollectionPageReceived.bind(this, onHaveCollectionsCallback);
                    this.fetch(overrideData, returnCallback);

                    return false;
                }
            }

            this._onCollectionPageReceived(onHaveCollectionsCallback);
        },

        _onCollectionPageReceived: function(onHaveCollectionsCallback) {

            // alert if we've just now received all collections
            this.checkHaveAllCollections();

            var pageNumber = this.getInputParam('offset');
            var countPerPage = this.getInputParam('limit');

            var returnData = {
                startPage: pageNumber,
                currentPage: pageNumber,
                countPerPage: countPerPage,
                collections: this._dataModel.get('collections').getSubset(pageNumber * countPerPage, countPerPage)
            };

            if (onHaveCollectionsCallback != undefined && typeof onHaveCollectionsCallback == 'function') {
                onHaveCollectionsCallback(returnData);
            }

            return returnData;
        },

        getAllCurrentCollectionsPages: function() {

            this.checkHaveAllCollections();

            var returnData = {
                startPage: 0,
                currentPage: this.getInputParam('offset'),
                countPerPage: this.getInputParam('limit'),
                collections: this._dataModel.get('collections').get()
            };

            return returnData;
        }

    });

    return GenericCollectionsDataFeed;

});