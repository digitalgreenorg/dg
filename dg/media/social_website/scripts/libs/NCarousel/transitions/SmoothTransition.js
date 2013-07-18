define(function(require) {
    'use strict';

    var Transition = require('libs/NCarousel/transitions/Transition');
    var Util = require('framework/Util');

    var SmoothTransition = Transition.extend({

        _state: null,

        constructor: function(carousel) {
            this.base(carousel);

            this._state = {
                speedScaler: -1
            };
        },

        _bindEvents: function() {

            // TODO: off() these in the destructor

            // bind a function to control the speed/direction of the carousel 
            // to the mousemove of the carousel container
            this._getDOMReference('carouselContainer')
                .on('mousemove', this._onMouseMove.bind(this));

            if (this._carouselConfig('pauseOnExit')) {
                this._getDOMReference('carouselContainer')
                    .on('mouseleave', this._onMouseLeave.bind(this));
            }
        },

        _onMouseMove: function(e) {

            if (this._carouselState('disableCarousel') == true) {
                return;
            }

            var $carouselWrapper = this._getDOMReference('carouselWrapper');
            var halfDistance;
            var relPos;

            if (this._direction == 'horizontal') {
                var halfDistance = $carouselWrapper.outerWidth() / 2;
                var relPos = e.pageX - $carouselWrapper.offset().left;
            } else {
                var halfDistance = $carouselWrapper.outerHeight() / 2;
                var relPos = e.pageY - $carouselWrapper.offset().top;
            }


            var centerOffset = relPos - halfDistance;
            var multiplier = (centerOffset < 0) ? -1 : 1;

            // adjust the speed scaler to allow some padding on either side so +-1 isn't right on the edge
            var speedScaler = centerOffset / (halfDistance * 0.83);

            // pad the middle area
            speedScaler -= 0.1 * multiplier;

            // detect the middle area and flatten the speed scaler to 0
            if (centerOffset * speedScaler <= 0) {
                speedScaler = 0;
            }

            // limit the speed scaler to +- 1
            if (Math.abs(speedScaler) > 1) {
                speedScaler = multiplier;
            }

            // flip!
            speedScaler *= -1;

            this._state.speedScaler = speedScaler.toFixed(2);
        },

        _onMouseLeave: function() {
            this._state.speedScaler = 0;
        },

        _prepareSlides: function() {
            this.base();
        },

        triggerTransition: function(newSlideNumber, options) {

            // start playing or stopped?
            if (!this._carouselConfig('autoPlay')) {
                this._state.speedScaler = 0;
            }


            var maxDistance;

            var axisSwitch;
            var orientationSwitch;

            if (this._carouselConfig('direction') == 'vertical') {
                axisSwitch = 'top';
                orientationSwitch = 'height';
                maxDistance = this._slideSize.height * this._numberOfSlides;
            } else {
                axisSwitch = 'left';
                orientationSwitch = 'width';
                maxDistance = this._slideSize.width * this._numberOfSlides;
            }

            var previousTime = new Date().getTime();

            var animationInterval = setInterval(function() {

                if (
                    this._disableCarousel == true || 
                    this._state.speedScaler == 0
                ) {
                    previousTime = new Date().getTime();
                    return;
                }

                var timeDifference = (new Date().getTime() - previousTime) / 1000;

                var newPos = this._$carouselList.position()[axisSwitch];
                newPos += (this._smoothTransitionSpeed * timeDifference * this._state.speedScaler);
                
                // determine behavior when reaching the end of the carousel based
                // on the value of smothCycle
                
                if (this._smoothCycle) {
                    // detect edge of the  carousel and adjust accordingly for loops
                    if (newPos < -1 * maxDistance) {
                        newPos += maxDistance;
                    } else if (newPos > 0) {
                        newPos -= maxDistance;
                    }
                } else {
                    if (newPos < this._containerSize[orientationSwitch] - maxDistance) {
                        newPos = this._containerSize[orientationSwitch] - maxDistance;
                    } else if (newPos > 0) {
                        newPos = 0;
                    }
                }

                this._$carouselList.css(axisSwitch, Math.round(newPos) + 'px');

                previousTime = new Date().getTime();

            }, 1000 / this._smoothTransitionFPS);

            
        }
    });

    return SmoothTransition;
});