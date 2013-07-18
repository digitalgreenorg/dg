/**
 * CollectionMostFiltersViewController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var Controller = require('framework/controllers/Controller');
    var jQuery = require('jquery');

    var CollectionMostFiltersViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();

            var references = this._references;
            references.$mostFiltersContainer = $referenceBase.find('.js-most-filters');
        },

        _initEvents: function() {
            this.base();

            var boundFunctions = this._boundFunctions;
            var references = this._references;

            boundFunctions.onMostFilterClick = this._onMostFilterClick.bind(this);
            references.$mostFiltersContainer.on('click', '.js-most-filter', boundFunctions.onMostFilterClick);
        },

        _onMostFilterClick: function(e) {
            e.preventDefault();

            var $currentTarget = jQuery(e.currentTarget);
            var newFilterId = $currentTarget.data('filter-id');

            this.setActiveFilter(newFilterId);
        },

        setActiveFilter: function(newFilterId) {
            var $mostFilters = this._references.$mostFiltersContainer.find('.js-most-filter');

            // get the previously active filter id
            var oldFilterId = $mostFilters.filter('.active').data('filter-id');

            // exit early if the filter hasn't changed
            // TODO: might we want the filter changing to be a toggle on/off?
            if (newFilterId == oldFilterId) {
            	this.setActiveFilter('-_score');
                return;
            }

            // get new filter element
            var $newFilterElement = $mostFilters.filter('[data-filter-id=' + newFilterId + ']');

            // clear active classes
            $mostFilters.removeClass('active');
            // add new active class
            $newFilterElement.addClass('active');

            // notify about the new filter
            this.trigger('orderChanged', newFilterId);
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

    return CollectionMostFiltersViewController;
});
