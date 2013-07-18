define(function(require) {
    'use strict';

    var LifeCycleBase = require('framework/LifecycleBase');

    var Transition = LifeCycleBase.extend({

        _carouselReference: null,
        _virtualNumberOfSlidesModifier: 0,

        constructor: function(carousel) {
            // store a reference to the carousel
            this._carouselReference = carousel;

            // bind events required for the transition
            this._bindEvents();

            // perform any preparation that must take place regarding the slides
            this._prepareSlides();
        },

        _bindEvents: function() {},

        _prepareSlides: function() {},

        reinitialize: function() {},

        getVirtaulNumberOfSlidesModifier: function() {
            return this._virtualNumberOfSlidesModifier;
        },

        /**
         * Proxy functions that act on the carousel reference
         */

        _getSlide: function(slideNumber) {
            return this._carouselReference.getSlide(slideNumber);
        },

        _getAllSlides: function() {
            return this._carouselReference.getAllSlides();
        },

        _cloneSlides: function(numberOfSlidesToClone) {
            this._carouselReference.cloneSlides(numberOfSlidesToClone);
        },

        _getCurrentSlideNumber: function() {
            return this._carouselReference.getCurrentSlideNumber();
        },

        _getNumberOfSlides: function() {
            return this._carouselReference.getNumberOfSlides();
        },

        _getContainerSize: function() {
            return this._carouselReference.getContainerSize();
        },

        _getSlideSize: function() {
            return this._carouselReference.getSlideSize();
        },

        _changeSlide: function(newSlideNumber, updateCurrentSlide, options) {
            this._carouselReference.changeSlide(newSlideNumber, updateCurrentSlide, options);
        },

        _getDOMReference: function(type) {
            return this._carouselReference.getDOMReference(type);
        },

        _carouselConfig: function(name, value, performValidation) {
            return this._carouselReference.config(name, value, performValidation);
        },

        _carouselState: function(name, value) {
            return this._carouselReference.state(name, value);
        },

        _slideChangeComplete: function(options) {
            this._carouselReference.slideChangeComplete(options);
        },









        triggerTransition: function() {}

    });

    return Transition;
});