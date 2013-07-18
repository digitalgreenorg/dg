define(function(require) {
    'use strict';

    var Transition = require('libs/NCarousel/transitions/Transition');
    var BasicTransition = require('libs/NCarousel/transitions/BasicTransition');
    var Util = require('framework/Util');

    var SlideTransition = Transition.extend({

        _virtualNumberOfSlidesModifier: 2,

        constructor: function(carousel) {
            this.base(carousel);

            this._basicTransition = new BasicTransition(this._carouselReference);
        },

        _prepareSlides: function() {

            this.base();

            var $carouselList = this._getDOMReference('carouselList');
            var $carouselSlides = this._getDOMReference('carouselSlides');
            var $firstSlide = $carouselSlides.eq(0);

            $carouselList.prepend($firstSlide.clone(true));
            $carouselList.prepend($firstSlide.clone(true));

        },

        triggerTransition: function(newSlideNumber, options) {

            var $carouselList = this._getDOMReference('carouselList');
            var $carouselSlides = $carouselList.find('> li');

            var slideNumber = newSlideNumber % (this._getNumberOfSlides());

            // copy slide 1 to slot 0
            $carouselSlides.eq(0).replaceWith($carouselSlides.eq(1).clone(true));

            // jump to slot 0 to prepare for transition
            this._changeSlide(0);

            // clone desired slide to slot 1
            var $clone = $carouselSlides.eq(slideNumber + 2).clone(true);
            $carouselSlides.eq(1).replaceWith($clone);

            // do transition
            this._basicTransition.triggerTransition(1, options);
            
        }
    });

    return SlideTransition;
});