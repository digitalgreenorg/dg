define([
    'libs/NCarousel/transitions/Transition'
],
function(
    Transition
) {
    "use strict";

    var BasicTransition = Transition.extend({
        constructor: function(carousel) {
            this.base(carousel);
        },

        _prepareSlides: function() {

        },

        triggerTransition: function(slideNumber, options) {
            this._changeSlide(slideNumber, true, options);
        }
    });

    return BasicTransition;
});