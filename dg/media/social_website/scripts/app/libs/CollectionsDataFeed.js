define(function(require) {
	'use strict';

	var DigitalGreenDataFeed = require('app/libs/DigitalGreenDataFeed');
	var DataModel = require('app/libs/DataModel');
	var Util = require('framework/Util');

	var CollectionsDataFeed = DigitalGreenDataFeed
			.extend({

				_filters : undefined,

				/*
				 * Input params:
				 * 
				 * searchString {string} filters {Object} orderBy {string} page
				 * {Number} count {Number} relativeUserId {string} (optional) --
				 * is this still needed?
				 * 
				 * Output params: collections {Collection[]} totalCount {Number}
				 */

				constructor : function($language) {
					this.base('api/elasticSearch/');

					this._filters = {};

					var dataModel = this._dataModel;

					// prepare data model
					var collectionsSubModel = dataModel.addSubModel(
							'collections', true);

					// set up input params
					
					this.addInputParam('searchString',false, 0, true)
					this.addInputParam('offset', true, 0, true);
					this.addInputParam('limit', true, 0, true);
					this.addInputParam('featured', true, 0, true);
					this.addInputParam('filters', false, null, true,
							collectionsSubModel);
					this.addInputParam('order_by', false, null, true,
							collectionsSubModel);
					//this.addInputParam('language__name', false, null, true)
					if ($language != -1){
					this.addInputParamCacheClear('language__name',
							collectionsSubModel);
						}
				},

				fetch : function(page, countPerPage) {
					if (page == undefined) {
						page = 0;
					}

					if (countPerPage == undefined) {
						countPerPage = 12;
					}

					this.setInputParam('offset', page * countPerPage, true);
					this.setInputParam('limit', countPerPage, true);
                    
					// perform the fetch
					this.base();
				},

				_processData : function(unprocessedData) {
					this.base(unprocessedData);

					// local references
					var dataModel = this._dataModel;
					var collectionsModel = dataModel.get('collections');

					// gather count and page for caching and saving purposes
					var countPerPage = unprocessedData.meta.limit;
					var page = unprocessedData.meta.offset
							/ unprocessedData.meta.limit;

					// store total count
					dataModel.set('totalCount',
							unprocessedData.meta.total_count);

					// import collections from data
					var collectionsToAdd = unprocessedData.objects;
					var startingCacheId = page * countPerPage;
					
					//facets
					var facets = unprocessedData.facets;
					dataModel.set('facets',
							unprocessedData.facets);

					collectionsModel.addSubset(collectionsToAdd,
							startingCacheId);
                    return collectionsToAdd;        
				},

				/**
				 * Sets the status and value of a filter
				 * 
				 * @param {Boolean}
				 *            filterParam The filter parameter
				 * @param {Boolean}
				 *            filterValue The filter value
				 * @param {Boolean}
				 *            active Whether or not the filter is active
				 * @return {boolean} true if a filter was changed, else false
				 */
				setFilterStatus : function(filterParam, filterValue, active) {

					var filters = this._filters;
					if (filters[filterParam] == undefined) {
						filters[filterParam] = [];
					}

					var filterIndex = filters[filterParam].indexOf(filterValue);
					var filterPresent = (filterIndex != -1);

					if ((active && filterPresent) || !active && !filterPresent) {
						return false;
					}

					// if we get here, a filter has changed
					// update accordingly

					if (active) {
						filters[filterParam].push(filterValue);
					} else {
						filters[filterParam].splice(filterIndex, 1);
					}

					// we now clone our filters object to not only reduce cross
					// class
					// referencing to this object, but also to trigger the
					// datafeed
					// to clear the cache since the reference will be changing

					var newFilters = Util.Object.clone(filters);
					this.setInputParam('filters', newFilters);
					return true;
				},

				/**
				 * Clears the search filters
				 * 
				 * @return {boolean} true if a filter was changed, else false
				 */
				clearFilters : function() {

					var filterExisted = false;

					var filters = this._filters;
					var filterKey;
					for (filterKey in filters) {
						var currentFilter = filters[filterKey];
						var len = currentFilter.length;
						if (len > 0) {
							filterExisted = true;
							break;
						}
					}

					this._filters = {};

					return filterExisted;
				},

				getTotalCount : function() {
					return this._dataModel.get('totalCount');
				},

				getCollections : function() {

					var page = this.getInputParam('offset');
					var countPerPage = this.getInputParam('limit');

					var collections = this._dataModel.get('collections')
							.getSubset(page * countPerPage, countPerPage);

					
					if (!collections) {
						this.fetch(page, countPerPage);
						return false;
					} 

					return collections;
				}

			});

	return CollectionsDataFeed;

});