define(function(require) {
    'use strict';

    var Transition = require('libs/NCarousel/transitions/Transition');
    var Util = require('framework/Util');

    var CycleTransition = Transition.extend({

        _slideOffset: 0,

        constructor: function(carousel) {
            this.base(carousel);
        },

        _prepareSlides: function() {
            this.base();

            var numberOfSlides = this._getNumberOfSlides();
            var containerSize = this._getContainerSize();
            var slideSize = this._getSlideSize();

            var clonesNecessary = Math.ceil(containerSize.width / (slideSize.width * numberOfSlides));

            // we need at least one full set of slides 
            // cloned for this transition to always work
            this._cloneSlides(clonesNecessary * numberOfSlides * 2);

            this._slideOffset = clonesNecessary * numberOfSlides;

            this._carouselState('slideOffset', this._slideOffset);

            // change the slide to the middle set
            this._changeSlide(
                this._slideOffset,
                false,
                {
                    preventSlideChangeCompleteEvent: true
                }
            );
        },

        triggerTransition: function(newSlideNumber, options) {

            if (options == null) {
                options = {
                    relativeOffset: 0
                }
            }

            // normalize the new slide number to a range we'd expect
            var currentSlideNumber = this._getCurrentSlideNumber();
            var numberOfSlides = this._getNumberOfSlides();

            var relativeOffset = options.relativeOffset;

            // normalize the slide number
            newSlideNumber = Util.Math.mod(newSlideNumber, numberOfSlides);

            if (options.directionReversed) {
                // always jump to the right-most copy of the current slide before transitioning
                this._changeSlide(
                    (currentSlideNumber % numberOfSlides) + numberOfSlides + this._slideOffset,
                    true,
                    {
                        preventSlideChangeCompleteEvent: true
                    }
                );

                if (currentSlideNumber > 0) {
                    newSlideNumber += numberOfSlides;
                }

            } else {
                // always jump to the left-most copy of the current slide before transitioning
                this._changeSlide(
                    (currentSlideNumber % numberOfSlides) + this._slideOffset,
                    true,
                    {
                        preventSlideChangeCompleteEvent: true
                    }
                );

                if (newSlideNumber < currentSlideNumber) {
                    newSlideNumber += numberOfSlides;
                }
            }

            // add the offset to the current and new slide number to keep the display in the middle
            newSlideNumber += this._slideOffset;

            // perform the transition
            this._changeSlide(newSlideNumber, true, options);
        }
    });

    return CycleTransition;
});
