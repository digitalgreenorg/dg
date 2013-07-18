/**
 * AboutController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var jQuery = require('jquery');

    var NCarousel = require('libs/NCarousel/NCarousel');

    var AboutController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {AboutController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            


            return this;
        },

        _initReferences: function($referenceBase, params) {
            this.base(params);

            var references = this._references;

            // dom elements
            references.$mainCarouselWrapper = jQuery('#main-carousel');

            references.mainCarousel = new NCarousel(references.$mainCarouselWrapper, {
                transition: 'slide',
                autoPlay: true,
                autoPlayDelay: 8000
            });
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return AboutController;
});
