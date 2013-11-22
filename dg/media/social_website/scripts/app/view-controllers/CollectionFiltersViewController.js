/**
 * CollectionFiltersViewController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var Controller = require('framework/controllers/Controller');
    var globalEventManager = require('framework/globalEventManager');
    var viewRenderer = require('framework/ViewRenderer');
    var Util = require('framework/Util');
    var jQuery = require('jquery');

    var SearchFiltersDataFeed = require('app/libs/SearchFiltersDataFeed');

    var collectionFilterListTemplate = require('text!app/views/collection-filter-list.html');
    var collectionFilterBreadcrumbsTemplate = require('text!app/views/collection-filter-breadcrumbs.html');

    var CollectionFiltersViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);

            this._fetchFilters();

            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;

            references.dataFeed = new SearchFiltersDataFeed();
            references.filters_cleared = 0;		// Initially clear filters is 0, so if any data-attributes present, use them

            references.$filtersWrapper = $referenceBase;
            references.$filtersContainer = $referenceBase.find('.js-filters-container');
            references.$filterBreadcrumbsContainer = jQuery('.js-filter-breadcrumbs');
        },

        _initState: function() {
            this.base();

            this._state.filterData = {};
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onFilterCategoryLabelClick = this._onFilterCategoryLabelClick.bind(this);
            references.$filtersContainer.on('click', '.js-filter-category-label', boundFunctions.onFilterCategoryLabelClick);

            boundFunctions.onFilterOptionClick = this._onFilterOptionClick.bind(this);
            references.$filtersContainer.on('click', '.js-filter-option', boundFunctions.onFilterOptionClick);

            boundFunctions.onBreadcrumbsRemoveFilterClick = this._onBreadcrumbsRemoveFilterClick.bind(this);
            references.$filterBreadcrumbsContainer.on('click', '.js-remove-filter', boundFunctions.onBreadcrumbsRemoveFilterClick);

            boundFunctions.onClearAllFiltersClick = this._onClearAllFiltersClick.bind(this);
            references.$filtersWrapper.on('click', '.js-clear-all-filters', boundFunctions.onClearAllFiltersClick);
        },

        _onFilterCategoryLabelClick: function(e) {
            e.preventDefault();

            var filterCategories = this._state.filterData.categories;
            var $newOpenFilterCategory = jQuery(e.currentTarget).closest('.js-filter-category');

            // if the category is already marked as open, exit
            var newOpenCategoryId = $newOpenFilterCategory.data('categoryId');

            if (filterCategories[newOpenCategoryId].categoryOpen) {
            	$newOpenFilterCategory.find('.js-subcategory-wrapper')
                .stop(true)
                .animate({
                    height: '0px'
                }, 1000);
            	$newOpenFilterCategory.removeClass('open');
            	filterCategories[newOpenCategoryId].categoryOpen = false;
                return;
            }

            // set the category open status of all categories to false
            var tmpCategoryId;
            for (tmpCategoryId in filterCategories) {
                filterCategories[tmpCategoryId].categoryOpen = false;
            }

            var $otherCategories = this._references.$filtersContainer
                .find('.js-filter-category')
                .not($newOpenFilterCategory);

            // hide the nested ul
            $otherCategories.find('.js-subcategory-wrapper')
                .stop(true)
                .animate({
                    height: '0px'
                }, 1000);

            // remove open class
            $otherCategories.removeClass('open');


            // set the new category status as open
            filterCategories[newOpenCategoryId].categoryOpen = true;

            // animate the new category open
            var $filterSubcategoryContainer = $newOpenFilterCategory.find('.js-subcategory-container');

            $newOpenFilterCategory.find('.js-subcategory-wrapper')
                .stop(true)
                .animate({
                    height: $filterSubcategoryContainer.outerHeight() + 'px'
                }, 1000);

            // add open class to new category
            $newOpenFilterCategory.addClass('open');
        },

        _onFilterOptionClick: function(e) {
            e.preventDefault();

            var $filterOption = jQuery(e.currentTarget);
            var $filterCategory = $filterOption.closest('.js-filter-category');

            var categoryId = $filterCategory.data('category-id');
            var optionId = $filterOption.data('option-id');

            // local reference
            var filterData = this._state.filterData;

            // get old value
            var oldValue = this._getFilterStatus(categoryId, optionId);

            // update data
            var newValue = !oldValue;

            this._setFilterStatus(categoryId, optionId, newValue);
            this._renderFilters();
        },

        _onBreadcrumbsRemoveFilterClick: function(e) {
            e.preventDefault();
            this._references.filters_cleared = 1; // on removal of any breadcrumb, remove usage of data-attributes

            var $breadcrumbItem = jQuery(e.currentTarget);

            var categoryId = $breadcrumbItem.data('categoryId');
            var optionId = $breadcrumbItem.data('optionId');

            this._setFilterStatus(categoryId, optionId, false);
            this._renderFilters();
        },

        _onClearAllFiltersClick: function(e) {
            e.preventDefault();

            this._clearFilters();
            this._references.$filtersContainer.find('.js-filter-option.enabled').removeClass('enabled');
            this._updateBreadcrumbs();

            this.trigger('filtersCleared');
        },

        _indicateCurrentLanguageSelection: function() {

            var currentLanguageCode = Util.Cookie.get('language__name');
            if (!currentLanguageCode) {
                return;
            }

            var languageCategory = this._state.filterData.categories.language;
            if (!languageCategory) {
                return;
            }

            // try/catch due to dynamic nature of filter data data structure
            try {
                var languageCategoryOptions = this._state.filterData.categories.language.options;
            } catch (e) {
                return;
            }

            var i = 0;
            var len = languageCategoryOptions.length;
            for (; i < len; i++) {
                if (languageCategoryOptions[i].value == currentLanguageCode) {
                    this._setFilterStatus('language__name', i, true);
                    return;
                }
            }
        },

        _clearFilters: function() {
            var filterData = this._state.filterData;
            if (filterData.categories == undefined) {
                return;
            }

            var categories = filterData.categories;

            var categoryId;
            var optionId;
            var optionsLength;
            for (categoryId in categories) {
                var currentCategory = categories[categoryId];
                var currentOptions = currentCategory.options;
                if (currentOptions == undefined) {
                    continue;
                }

                optionId = 0;
                optionsLength = currentOptions.length;
                for (; optionId < optionsLength; optionId++) {
                    var currentOption = currentOptions[optionId];
                    if (!currentOption.filterActive) {
                        continue;
                    }

                    currentOption.filterActive = false;
                }
            }
        },

        updateTotalCount: function(totalCount) {
            this._state.totalCount = totalCount;
            this._updateBreadcrumbs();
        },

        _updateBreadcrumbs: function() {
            var activeFilters = this._getActiveFilters();

            // formulate data to pass to renderer
            var renderData = {
                totalCount: this._state.totalCount,
                activeFilters: activeFilters
            };

            viewRenderer.renderHTML(this._references.$filterBreadcrumbsContainer, collectionFilterBreadcrumbsTemplate, renderData);
        },

        // TODO: $filterOption not used any more -- marked for removal?
        // _setFilterStatus: function($filterOption, categoryId, optionId, value) {
        _setFilterStatus: function(categoryId, optionId, value) {
            // TODO: not used any more -- marked for removal?
            // if ($filterOption == undefined) {
            //     $filterOption = this._findFilterElementById(categoryId, optionId);
            // }

            // local references
        	//remove once the discrepancy bw language/language_name is solved
        	if(categoryId=='language__name'){
        		categoryId='language';
        	}
        	var i;
            var filterCategoryData = this._state.filterData.categories[categoryId];
            var filterOptionData;
        	for (i=0; i < filterCategoryData.options.length; i++){
        		if (filterCategoryData.options[i].title == optionId){
        			filterOptionData = this._state.filterData.categories[categoryId].options[i];
        		}
        	}
        	
            if (filterOptionData == undefined){
            	return;
            }
            // update value
            filterOptionData.filterActive = value;
            
            this._updateBreadcrumbs();

            // alert a value change
            this.trigger('filterChanged', categoryId, filterOptionData.value, value);
        },

        _getFilterStatus: function(categoryId, optionId) {
        	var i;
        	for (i=0; i < this._state.filterData.categories[categoryId].options.length; i++){
        		if (this._state.filterData.categories[categoryId].options[i].title == optionId){
        			return this._state.filterData.categories[categoryId].options[i].filterActive
        		}
        	}
            
        },

        _findFilterElementById: function(categoryId, optionId) {
            var $filtersContainer = this._references.$filtersContainer;

            var $filterCategory = $filtersContainer.find('[data-category-id=' + categoryId + ']');
            var $filterOption = $filterCategory.find('[data-option-id=' + optionId + ']');

            return $filterOption;
        },

        _fetchFilters: function() {
            this._references.dataFeed.fetch(null, this._onDataProcessed.bind(this));
        },

        _onDataProcessed: function() {
            this._state.filterData = this._references.dataFeed.getSearchFilters();
            //this._indicateCurrentLanguageSelection();
            this._renderFilters();
        },

        _getFilterDataForRender: function() {

            var filterData = this._state.filterData;

            var categoriesForRender = [];

            var currentActiveFilters = this._getActiveFilters();

            var categories = filterData.categories;
            
            var i;
            
            var filterorder = ['state', 'language', 'partner', 'category', 'subcategory', 'topic', 'subject'];
            
            var index;
            
            for (index in filterorder) {
            	var categoryId = filterorder[index]; 
                
            	var currentCategory = Util.Object.clone(categories[categoryId], true);
                currentCategory._categoryId = categoryId;

                var options = currentCategory.options;

                for (i = 0; i < options.length; i++) {
                    var currentOption = options[i];
                    
                    if (currentOption.dependencies) {
                        var dependenciesMet = this._checkFilterDependcies(currentOption.dependencies);
                        
                        if (!dependenciesMet) {
                            options.splice(i, 1);
                            // we removed an option from the array which will decrease the length of the array
                            // as well as change the indexing; thus, we subtract 1 from the iterator
                            i--;
                            continue;
                        }
                    }

                    currentCategory.options[i]._optionId = i;
                }
                
                categoriesForRender.push(currentCategory);
            }



            var filterDataForRender = {
                categories: categoriesForRender
            };

            return filterDataForRender;
        },

        _checkFilterDependcies: function(dependencies) {
            return (this._checkFilterAllOfDependencies(dependencies.allOf) && this._checkFilterOneOfDependencies(dependencies.oneOf));
        },

        _checkFilterAllOfDependencies: function(dependenciesAllOf) {

            if (dependenciesAllOf == undefined) {
                return true;
            }

            var categories = this._state.filterData.categories;

            var categoryId;

            for (categoryId in dependenciesAllOf) {
                // if the category we have a dependency on doesn't exist, exit
                if (!(categoryId in categories)) {
                    return false;
                }

                var currentDependencyArray = dependenciesAllOf[categoryId];
                var i = 0;
                var currentDependencyArrayLength = currentDependencyArray.length;
                for (; i < currentDependencyArrayLength; i++) {

                    var currentDependencyValue = currentDependencyArray[i];

                    var categoryOptions = categories[categoryId].options;

                    var dependencyFound = false;

                    var j = 0;
                    var categoryOptionsLength = categoryOptions.length;
                    for (; j < categoryOptionsLength; j++) {
                        var currentDependencyOption = categoryOptions[j];

                        // if the option we're currently looking at isn't what we're looking for, continue and keep looking
                        if (currentDependencyValue != currentDependencyOption.value) {
                            continue;
                        }

                        // if we make it this far, we've found the option we're looking for
                        // if it's not enabled, we haven't met all of the dependencies
                        if (!currentDependencyOption.filterActive) {
                            return false;
                        }

                        // we've now found the option we're looking for, and it's enabled
                        // we track this so we can ensure we've found it after this loop finishes, and stop looking
                        dependencyFound = true;
                        break;
                    }

                    if (!dependencyFound) {
                        return false;
                    }
                }
            }

            return true;
        },

        _checkFilterOneOfDependencies: function(dependenciesOneOf) {

            if (dependenciesOneOf == undefined) {
                return true;
            }

            var categories = this._state.filterData.categories;

            var categoryId;

            for (categoryId in dependenciesOneOf) {
                // if the category we have a dependency on doesn't exist, exit
                if (!(categoryId in categories)) {
                    return false;
                }

                var dependencyMet = false;

                var currentDependencyArray = dependenciesOneOf[categoryId];
                var i = 0;
                var currentDependencyArrayLength = currentDependencyArray.length;
                for (; i < currentDependencyArrayLength; i++) {

                    var currentDependencyValue = currentDependencyArray[i];

                    var categoryOptions = categories[categoryId].options;

                    var j = 0;
                    var categoryOptionsLength = categoryOptions.length;
                    for (; j < categoryOptionsLength; j++) {
                        var currentDependencyOption = categoryOptions[j];

                        if ((currentDependencyValue == currentDependencyOption.value) && currentDependencyOption.filterActive) {
                            dependencyMet = true;
                            break;
                        }
                    }

                    if (dependencyMet) {
                        break;
                    }
                }

                if (!dependencyMet) {
                    return false;
                }
            }

            return true;
        },

        _renderFilters: function() {
            var filterDataForRender = this._getFilterDataForRender();
            viewRenderer.renderHTML(this._references.$filtersContainer, collectionFilterListTemplate, filterDataForRender);
        },

        _getActiveFilters: function() {

            var activeFilters = [];

            var filterData = this._state.filterData;
            if (filterData.categories == undefined) {
                return [];
            }

            var categories = filterData.categories;
            
            var categoryId;
            var optionId;
            var optionsLength;
            for (categoryId in categories) {
                var currentCategory = filterData.categories[categoryId];
                var currentOptions = currentCategory.options;
                if (currentOptions == undefined) {
                    continue;
                }

                optionId = 0;
                optionsLength = currentOptions.length;
                for (; optionId < optionsLength; optionId++) {
                    var currentOption = currentOptions[optionId];
                    if (!currentOption.filterActive) {
                        continue;
                    }

                    activeFilters.push({
                        title: currentOption.title,
                        categoryId: categoryId,
                        optionId: optionId
                    });
                }
            }

            return activeFilters;
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();

            // TODO: clean up
        }
    });

    return CollectionFiltersViewController;
});
