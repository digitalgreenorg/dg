define([
    'libs/NCarousel/transitions/Transition'
],
function(
    Transition
) {
    "use strict";

    var FadeTransition = Transition.extend({
        constructor: function(carousel) {
            this.base(carousel);
        },

        _prepareSlides: function() {
            var $carouselSlides = this._getAllSlides();

            $carouselSlides.css({
                // display: 'none',
                position: 'absolute',
                top: 0,
                left: 0,
                opacity: 0
            });

            $carouselSlides.eq(0).css({
                display: 'block',
                opacity: 1,
                zIndex: 2
            });

            this._setCarouselListSize();
        },

        reinitialize: function() {
            this._setCarouselListSize();
        },

        _setCarouselListSize: function() {
            var $carouselList = this._getDOMReference('carouselList');
            var $carouselSlides = this._getAllSlides();

            var maxHeight = 0;

            for (var i = 0, len = $carouselSlides.length; i < len; i++) {
                var currentSlideHeight = $carouselSlides.eq(i).outerHeight(true, true);
                if (currentSlideHeight > maxHeight) {
                    maxHeight = currentSlideHeight;
                }
            }

            if (maxHeight > 0) {
                $carouselList.css('height', maxHeight + 'px');
            }
        },

        triggerTransition: function(slideNumber, options) {

            if (options == null) {
                options = {};
            }

            // TODO: implement fade time			
            options.fadeTime = options.fadeTransitionSpeed;			

            var currentSlideNumber = this._getCurrentSlideNumber();

            // if the slide hasn't changed (carousel reinitialized, etc.), we
            // don't need to redraw
            if (currentSlideNumber == slideNumber) {
                return;
            }

            var $oldSlide = this._getSlide(currentSlideNumber);
            var $newSlide = this._getSlide(slideNumber);

            $oldSlide
                .css({
                    zIndex: ''
                })
                .stop(true, true);

            // animate new slide in
            $newSlide
                .stop(true, true)
                .css({
                    display: 'block',
                    zIndex: 1
                })
                .animate({
                    opacity: 1
                },
                options.fadeTime,
                this._onTransitionComplete.bind(this, $oldSlide));
        },

        _onTransitionComplete: function($oldSlide) {
            $oldSlide.css({
                display: 'none',
                opacity: 0
            });

            this._slideChangeComplete();
        }
    });

    return FadeTransition;
});