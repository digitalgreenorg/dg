/*

*** carousel orientation
direction:                      ENUM['vertical', 'horizontal', 'up', 'down', 'left', 'right']

*** transition type
transition:                     ENUM['basic', 'cycle', 'fade', slide', 'smooth']

*** true | false | 1 | 0
autoPlay:                       BOOL

*** true | false | 1 | 0
pauseOnHover:                   BOOL

*** true | false | 1 | 0
pauseOnExit:                    BOOL

*** true | false | 1 | 0
advanceOnClick:                 BOOL

*** true | false | 1 | 0
showAllOnClick:                 BOOL

*** numeric in ms
showAllTransitionSpeed:         UINT

*** numeric, number of slides per autoplay transition (positive/negative for direction)
autoPlayStep:                   INT

*** numeric in ms
scrollSpeed:                    UINT

*** numeric in ms
autoPlayDelay:                  UINT

*** numeric in pixels/second
fadeTransitionSpeed:            UINT

*** numeric in pixels/second
smoothTransitionSpeed:          UINT

*** allows infinite loop of items in carousel
smoothCycle:                    BOOL

*** true | false | 1 | 0
disableControlsOnChange:        BOOL

*** true | false | 1 | 0
disableAutoPlayOnUserAction:    BOOL

*** sets whether or not the carousel is allowed to wrap once reaching the beginning/end
allowWrapping:                  BOOL

*** sets aspect ratio to conform to when resizing carousel
aspectRatio:                    NUMBER

*** whether or not to bind swipe events
bindSwipeEvents:                BOOL

*** array of functions to call on slide change
onSlideChangeEvents:

*** array of functions to call periodically during slide delay interval
autoPlayProgressEvents:

*/


define(function(require) {
    'use strict';

    var jQuery = require('jquery');
    var ConfigurationManager = require('libs/general/ConfigurationManager/ConfigurationManager');
    var Validator = require('libs/general/Validator');
    var SwipeManager = require('libs/general/Swipe/SwipeManager');
    
    // transitions
    var BasicTransition = require('libs/NCarousel/transitions/BasicTransition');
    var CycleTransition = require('libs/NCarousel/transitions/CycleTransition');
    var FadeTransition = require('libs/NCarousel/transitions/FadeTransition');
    var SlideTransition = require('libs/NCarousel/transitions/SlideTransition');
    var SmoothTransition = require('libs/NCarousel/transitions/SmoothTransition');

    var NCarousel = function($carouselWrapper, params) {
        this.constructor($carouselWrapper, params);
    }

    NCarousel.prototype = {

        // TODO: reorganize
        // !!! new
        _carouselConfiguration: null,
        _transitionObject: null,
        _swipeManager: null,

        
        _domReferences: null,


        // object to hold state related variables
        _state: null,




        // from configuration, for internal use
        _autoPlayProgressEvents: null,
        _onSlideChangeEvents: null,


        // internal use
        _containerSize: null,
        _slideSize: null,
        _carouselReversed: false,
        _numberOfSlides: 0,
        _virtualNumberOfSlides: 0,
        _smoothTransitionFPS: 60,
        _autoPlayProgressFPS: 30,




        constructor: function($carouselWrapper, userConfiguration) {

            // check to see if this element has already had NCarousel initialized on it
            var carouselWrapperDataNCarousel = $carouselWrapper.data('NCarousel');
            if (carouselWrapperDataNCarousel && carouselWrapperDataNCarousel instanceof NCarousel) {
                return false;
            }

            if (userConfiguration == undefined) {
                userConfiguration = {};
            }

            // TODO: move these
            this._state = {
                previousAutoPlaySlideChangeTime: null,
                disableCarousel: false,
                disableAutoPlay: false,
                currentSlideNumber: 0,
                changingSlide: false,

                slideOffset: 0,

                // timeouts / intervals
                autoPlayInterval: null
            };
            
            // import user configuration
            this._initConfiguration(userConfiguration);

            /*
             * Manual processing of user provided values/options
             */

            // if we have an direction other than horizontal or vertical, 
            // we need to do some additional checking
            if (!this._carouselConfiguration.isOptionValid('direction')) {
                // detect if reversal is necessary
                if (userConfiguration.direction == 'right' || userConfiguration.direction == 'down') {
                    this._carouselReversed = true;
                }

                // normalize to horizontal/vertical
                if (userConfiguration.direction == 'left' || userConfiguration.direction == 'right') {
                    this.config('direction', 'horizontal');
                } else if (userConfiguration.direction == 'up' || userConfiguration.direction == 'down') {
                    this.config('direction', 'vertical');
                }
            }

            if (userConfiguration.onSlideChange != null) {
                if (typeof userConfiguration.onSlideChange == 'function') {
                    userConfiguration.onSlideChange = [userConfiguration.onSlideChange];
                }

                this._onSlideChangeEvents = userConfiguration.onSlideChange;
            }

            if (userConfiguration.onAutoPlayProgress !== undefined) {
                if (typeof userConfiguration.autoPlayProgress == 'function') {
                    userConfiguration.autoPlayProgress = [userConfiguration.autoPlayProgress];
                }

                this._autoPlayProgressEvents = userConfiguration.autoPlayProgress;
            }

            /*
             * Done handling most params
             */




            // set up internal references
            this._storeReferences($carouselWrapper);

            // gather information about number of slides, slide sizes, etc.
            this._calculateNumberOfSlides();

            // TODO: why is this necessary again?
            // safeguard against errors by ensuring we have slides
            if (this._numberOfSlides == 0) {
                return;
            }

            // bind carousel events
            this._bindEvents();

            // attach dynamically generated classes onto carousel markup items  
            this._attachClasses();

            // perform first calculation of the carousel size
            // this is done here because some transitions need this information
            // to intiailize properly
            this.resizeCarouselList();

            // initialize the transition to be used with this carousel
            this._initTransition();

            // we make another call to the resize function here to
            // ensure the carousel list is wide enough to display all slides
            // this is necessary because some transitions may cause 
            // a change in the virtual number of slides, and thus the overall
            // width of the carousel list must be adjusted
            this.resizeCarouselList();

            this.updateNavigation();
            this.updateIndicators();

            // TODO: this wasn't being called for all transitions before -- should it be now?
            if (this.config('autoPlay')) {
                this.startAutoPlay();
            }

            // hide the loading indicator if present
            this.getDOMReference('carouselContainer')
                .find('.carousel-loading')
                    .hide();
			
			this.state('carouselInitialized', true);

            $carouselWrapper.data('NCarousel', this);
        },

        _reinitializeCarousel: function() {
            this._storeReferences(this.getDOMReference('carouselWrapper'));

            this._calculateNumberOfSlides();
            this._attachClasses();

            this._transitionObject.reinitialize();

            this.resizeCarouselList();

            this.updateNavigation();
            this.updateIndicators();

            this.changeSlide(0, true);
        },


        _initConfiguration: function(userConfiguration) {

            this._carouselConfiguration = new ConfigurationManager();

            // carousel orientation
            this._carouselConfiguration
                .addOption('direction')
                .setAllowedValues(['vertical', 'horizontal'])
                .setDefaultValue('horizontal');

            // transition type
            this._carouselConfiguration
                .addOption('transition')
                .setAllowedValues(['basic', 'cycle', 'fade', 'slide', 'smooth'])
                .setDefaultValue('basic');

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('autoPlay')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('pauseOnHover')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('pauseOnExit')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('advanceOnClick')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(false);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('showAllOnClick')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(false);

            // numeric in ms
            this._carouselConfiguration
                .addOption('showAllTransitionSpeed')
                .setValidationType(Validator.VALIDATION_TYPES.UINT)
                .setDefaultValue(500);

            // numeric, number of slides per autoplay transition (positive/negative for direction)
            this._carouselConfiguration
                .addOption('autoPlayStep')
                .setValidationType(Validator.VALIDATION_TYPES.INT)
                .setDefaultValue(1);

            // numeric in ms
            this._carouselConfiguration
                .addOption('scrollSpeed')
                .setValidationType(Validator.VALIDATION_TYPES.UINT)
                .setDefaultValue(1000);

            // numeric in ms
            this._carouselConfiguration
                .addOption('autoPlayDelay')
                .setValidationType(Validator.VALIDATION_TYPES.UINT)
                .setDefaultValue(3000);

            // numeric in pixels/second
            this._carouselConfiguration
                .addOption('fadeTransitionSpeed')
                .setValidationType(Validator.VALIDATION_TYPES.UINT)
                .setDefaultValue(1000);
            
            // numeric in pixels/second
            this._carouselConfiguration
                .addOption('smoothTransitionSpeed')
                .setValidationType(Validator.VALIDATION_TYPES.UINT)
                .setDefaultValue(100);

            // allows infinite loop of items in carousel
            this._carouselConfiguration
                .addOption('smoothCycle')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('disableControlsOnChange')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // true | false | 1 | 0
            this._carouselConfiguration
                .addOption('disableAutoPlayOnUserAction')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // array of functions to call on slide change
            this._carouselConfiguration
                .addOption('onSlideChangeEvents')
                .setDefaultValue(null);

            // array of functions to call periodically during slide delay interval
            this._carouselConfiguration
                .addOption('autoPlayProgressEvents')
                .setDefaultValue(null);

            // sets whether or not the carousel is allowed to wrap once reaching the beginning/end
            this._carouselConfiguration
                .addOption('allowWrapping')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(true);

            // swipe event binding
            this._carouselConfiguration
                .addOption('bindSwipeEvents')
                .setValidationType(Validator.VALIDATION_TYPES.BOOL)
                .setDefaultValue(false);

            // whether or not the carousel should maintain aspect ratio when being resized
            this._carouselConfiguration
                .addOption('aspectRatio')
                .setValidationType(Validator.VALIDATION_TYPES.NUMBER)
                .setDefaultValue(null);

            this._carouselConfiguration.importConfiguration(userConfiguration);
            this._carouselConfiguration.validate();
        },

        _storeReferences: function($carouselWrapper) {

            // init storage object
            this._DOMReferences = {};

            // store the wrapper
            this._DOMReferences.$carouselWrapper = $carouselWrapper;

            // store the carousel container div (contains the carousel list)
            this._DOMReferences.$carouselContainer = this.getDOMReference('carouselWrapper').find('.js-carousel-container').eq(0);

            // store the carousel ul element for later use
            this._DOMReferences.$carouselList = this.getDOMReference('carouselContainer').children('ul');

            // store the slides for later use
            this._DOMReferences.$carouselSlides = this.getDOMReference('carouselList').children('li');

            // store the carousel navigation if present
            this._DOMReferences.$carouselNav = this.getDOMReference('carouselWrapper').find('.js-carousel-nav');
        },

        getDOMReference: function(type) {
            if ('$' + type in this._DOMReferences) {
                return this._DOMReferences['$' + type];
            }

            return null;
        },

        _calculateNumberOfSlides: function() {
            // store number of slides
            this._numberOfSlides = this._virtualNumberOfSlides = this.getDOMReference('carouselSlides').size();

            if (this._transitionObject) {
                this._virtualNumberOfSlides += this._transitionObject.getVirtaulNumberOfSlidesModifier();
            }
        },

        cloneSlides: function(numberOfSlidesToClone) {
            // clone slides as necessary obeying order depending on carouselReversed status
            if (this._carouselReversed) {
                for (var i = 0; i < numberOfSlidesToClone; i++) {
                    this.getDOMReference('carouselList').prepend(this.getDOMReference('carouselSlides').get(this._numberOfSlides - (i % this._numberOfSlides) - 1).cloneNode(true));
                    this._virtualNumberOfSlides++;
                }
            } else {
                for (var i = 0; i < numberOfSlidesToClone; i++) {
                    this.getDOMReference('carouselList').append(this.getDOMReference('carouselSlides').get(i % this._numberOfSlides).cloneNode(true));
                    this._virtualNumberOfSlides++;
                }
            }
        },

        resizeCarouselList: function() {
            // TODO: this needs to be tested/filled out for vertical scrolling carousels

            this._calculateNumberOfSlides();

            var $carouselContainer = this.getDOMReference('carouselContainer');
            var $carouselList = this.getDOMReference('carouselList');
            var $carouselSlides = this.getDOMReference('carouselSlides');

            // reset the size of the container, list, and slides
            this.resetSize($carouselContainer);
            this.resetSize($carouselList, true, false);
            this.resetSize($carouselSlides);

            // TODO: this needs testing with other transitions (use of inner/outer)
            // get the size of the carousel container (including padding and border)
            var containerSize = this._containerSize = this.getSize($carouselContainer, 'inner', true);

            // get the size of the carousel's slides
            var slideSize = this._slideSize = this.getSize($carouselSlides, 'outer', true, true, true);

            // before updating the width of the carousel list, set the size
            // of the slides; this is done to handle cases where a non-pixel
            // unit is used to define the width of the slides
            $carouselSlides.css('width', slideSize.baseWidth + 'px');

            // if horizontal scrolling mode, expand the size of the 
            // ul to fit all elements
            if (this.config('direction') == 'horizontal') {
                // TODO: look over this calculation -- it's not exact, and may 
                // exhibit problems in future implementations
                // calculate the width
                $carouselList.css('width', (slideSize.width * this._virtualNumberOfSlides) + (containerSize.width - containerSize.baseWidth));
            }

            var aspectRatio = this.config('aspectRatio');
            if (aspectRatio && Validator.validate(aspectRatio, Validator.VALIDATION_TYPES.NUMBER)) {
                $carouselContainer.css('height', Math.floor(containerSize.baseWidth / aspectRatio) + 'px');
                $carouselSlides.css('height', Math.floor(slideSize.baseWidth / aspectRatio) + 'px');
            }
        },

        resetSize: function($element, width, height) {

            if (width == null) {
                width = true;
            }

            if (height = null) {
                height = true;
            }

            if (width) {
                $element.css({
                    width: ''
                });
            }

            if (height) {
                $element.css({
                    height: ''
                });
            }
        },



        /**
         * Wrapper similar to jQuery's outerWidth(), allowing for
         * specification of which style attributes to take into
         * consideration in calculations.
         */
        getSize: function($element, innerOrOuter, addPadding, addMargin, addBorder) {

            var width = null;
            var height = null;

            if (innerOrOuter == 'inner') {
                width = $element.width();
                height = $element.height();
            } else {
                width = $element.outerWidth();
                height = $element.outerHeight();
            }

            var calculatedWidth = width;
            var calculatedHeight = height;

            if (addPadding) {
                calculatedWidth +=  parseInt($element.css('padding-left'), 10) +
                                    parseInt($element.css('padding-right'), 10);

                calculatedHeight += parseInt($element.css('padding-top'), 10) +
                                    parseInt($element.css('padding-bottom'), 10);
            }

            if (addMargin) {
                calculatedWidth +=  parseInt($element.css('margin-left'), 10) +
                                    parseInt($element.css('margin-right'), 10);

                calculatedHeight += parseInt($element.css('margin-top'), 10) +
                                    parseInt($element.css('margin-bottom'), 10);
            }

            if (addBorder) {
                calculatedWidth +=  parseInt($element.css('border-left-width'), 10) +
                                    parseInt($element.css('border-right-width'), 10);

                calculatedHeight += parseInt($element.css('border-top-width'), 10) +
                                    parseInt($element.css('border-bottom-width'), 10);
            }

            var returnObj = {
                baseWidth: width,
                baseHeight: height,
                width: calculatedWidth,
                height: calculatedHeight
            };

            return returnObj;
        },

        getContainerSize: function() {
            return this._containerSize;
        },

        getSlideSize: function() {
            return this._slideSize;
        },





















        // TODO: move this
        _onUserAction: function() {
            if (this.config('disableAutoPlayOnUserAction')) {
                this.disableAutoPlay();
            }
        },

        _onNavigationItemClick: function(slideIndex, e) {
            // e.preventDefault(); TODO: Make this so the "Read More" link on the main carousel tabs can be clickable
            
            this._onUserAction();
            
            // Read More links determine the click event now- 10/18/2012
            // We must detect the slide links and try to transition gracefully to the next page
            //if (slideIndex == this.state('currentSlideNumber')){
            //    var possibleLink = $('.carousel-nav-item.carousel-nav-item-' + (this.state('currentSlideNumber') + 1)).find('a.content-carousel-read-more');
            //   if (possibleLink.length) {
            //        e.preventDefault();
            //        window.location.href = possibleLink.attr('href');
            //
            //    }
            //}

            this.moveToSlide(slideIndex,
            {
                stopAutoPlay: false
            });
        },

        _onPreviousNextSlideClick: function(offset, e) {
            e.preventDefault();
            
            this._onUserAction();

            this.moveRelativeToSlide(offset);
        },

        // TODO: test this
        _onAdvanceSlideClick: function(e) {
            e.preventDefault();

            this._onUserAction();

            var $target = jQuery(e.target);
            if (e.target.tagName != 'A' || ($target.data('events') && $target.data('events').click !== undefined)) {
                e.preventDefault();
                this.moveRelativeToSlide(1);
            }
        },

        // TODO: test this
        _onShowFullSlide: function(e) {
            e.preventDefault();

            var $target = jQuery(e.target);
            var slideVisibility = this.fullSlideIsVisible($target);

            if (slideVisibility !== true) {
                if (slideVisibility.left < 0) {
                    this._$carouselList.animate({left: this._$carouselList.position().left - slideVisibility.left}, this._showAllTransitionSpeed);
                } else {
                    this._$carouselList.animate({left: this._$carouselList.position().left + slideVisibility.right}, this._showAllTransitionSpeed);
                }
            }
        },



        _bindEvents: function() {

            if (this.config('bindSwipeEvents')) {
                this._bindSwipeEvents();
            }

            // if a nav is present
            if (this.getDOMReference('carouselNav').size() > 0) {
                // select generic to allow any tags to be used to mark up the nav
                var $navSlides = this.getDOMReference('carouselNav').children().eq(0).children();
                if ($navSlides.size() > 0) {
                    // use supplied li elements for slide changing
                    for (var slideIndex = 0, slidesLength = $navSlides.size(); slideIndex < slidesLength; slideIndex++) {
                        $navSlides.eq(slideIndex)
                            .click(this._onNavigationItemClick.bind(this, slideIndex))
                            .mousedown(function(e) {
                                e.preventDefault();
                            });
                    }
                } else {
                    // TODO: auto generate slide changing elements?
                    // by appending a ul with li elements for each slide
                }
            }

            // bind "Previous Slide" element click if present
            this.getDOMReference('carouselWrapper')
                .find('.js-carousel-previous-slide')
                    .click(this._onPreviousNextSlideClick.bind(this, -1))
                    .mousedown(function(e) {
                        e.preventDefault();
                    });

            // bind "Next Slide" element click if present
            this.getDOMReference('carouselWrapper')
                .find('.js-carousel-next-slide')
                    .click(this._onPreviousNextSlideClick.bind(this, 1))
                    .mousedown(function(e) {
                        e.preventDefault();
                    });

            // attach click to advance functionality if desired
            if (this.config('advanceOnClick')) {
                this.getDOMReference('carouselList')
                    .addClass('advance-on-click')
                    .on('click', '> li', this._onAdvanceSlideClick.bind(this));
            }

            // attach click to make visible functionality if desired
            // if enabled and the user clicks a slide that is not fully visible, this will move the full slide into view
            // TODO: what if the slide is bigger than the carousel viewport?
            if (this.config('transition') == 'smooth' && this.config('showAllOnClick')) {
                this.getDOMReference('carouselList')
                    .on('click', '> li', this._onShowFullSlide.bind(this));
            }

            


            jQuery(window).on('resize', this._onResize.bind(this));


        },

        _bindSwipeEvents: function() {

            var swipeManager = this._swipeManager = new SwipeManager();
            var swipeListener = this._swipeManager.addListener(this.getDOMReference('carouselContainer'));

            swipeListener.addEventListener('swipeStart', this.stopAutoPlay.bind(this));

            var swipeLeftOptions = {
                swipeType:              swipeManager.SWIPE_TYPES.LEFT,
                swipeDistance:          100, 
                swipeUnits:             swipeManager.SWIPE_UNITS.PIXELS, 
                triggerOnlyOnRelease:   false, 
                callback:               this._onSwipe.bind(this, 1)
            };

            var swipeRightOptions = {
                swipeType:              swipeManager.SWIPE_TYPES.RIGHT,
                swipeDistance:          100, 
                swipeUnits:             swipeManager.SWIPE_UNITS.PIXELS, 
                triggerOnlyOnRelease:   false, 
                callback:               this._onSwipe.bind(this, -1)
            };

            swipeListener
                .addSwipeConfiguration(swipeLeftOptions)
                .addSwipeConfiguration(swipeRightOptions);
        },

        _onSwipe: function(relativeOffset, swipeInformation) {
            this.moveRelativeToSlide(relativeOffset);
        },

        _onResize: function() {
            // TODO: compare against last width height?
            // TODO: reset to slide 0 on resize?

            var newWindowSize = this._windowSizeChanged();

            if (newWindowSize) {
                this.resizeCarouselList();
                
                this.resetCurrentSlide();

                this.state('windowWidth', newWindowSize.width);
                this.state('windowHeight', newWindowSize.height);
            }
        },

        _windowSizeChanged: function() {
            var $window = jQuery(window);

            var currentWidth = $window.width();
            var currentHeight = $window.height();

            if (this.state('windowWidth') != currentWidth || this.state('windowHeight') != currentHeight) {
                return {
                    width: currentWidth,
                    height: currentHeight
                }
            }

            return false;
        },

        _attachClasses: function() {

            // if horizontal direction, ensure horizontal class is added
            if (this.config('direction') == 'horizontal') {
                this.getDOMReference('carouselWrapper').addClass('carousel-horizontal');
            }

            // add item classes for styling/other purposes
            var $carouselItems = this.getDOMReference('carouselList').children('li');

            // remove all previously attached carousel classes
            $carouselItems.removeClass (function (index, css) {
                return (css.match (/\bcarousel-item-\S+/g) || []).join(' ');
            });

            for (var i = 0, len = $carouselItems.length; i < len; i++) {
                $carouselItems.eq(i)
                    .addClass('carousel-item')
                    .addClass('carousel-item-' + (i + 1));
            }

            // flip the order of the carousel items if the list is reversed
            if (this._carouselReversed) {
                for (var i = 0, len = $carouselItems.length; i < len; i++) {
                    this._$carouselList.prepend($carouselItems.get(i));
                }
            }

            // if a nav is present, find the nav items and add classes
            var $carouselNav = this.getDOMReference('carouselNav');
            if ($carouselNav) {
                var $navItems = $carouselNav.children().children();

                // remove all previously attached carousel classes
                $navItems.removeClass (function (index, css) {
                    return (css.match (/\bcarousel-nav-item-\S+/g) || []).join(' ');
                });

                for (var i = 0, len = $navItems.length; i < len; i++) {
                    $navItems.eq(i)
                        .addClass('carousel-nav-item')
                        .addClass('carousel-nav-item-' + (i + 1));
                }

            }

            // ensure position relative on needed elements
            this.getDOMReference('carouselContainer').css('position', 'relative');
            this.getDOMReference('carouselList').css('position', 'relative');

        },



        _initTransition: function() {
            var transition = this.config('transition');

            switch (transition) {
                case 'basic':
                    this._transitionObject = new BasicTransition(this);
                    break;
                case 'cycle':
                    this._transitionObject = new CycleTransition(this);
                    break;
                case 'fade':
                    this._transitionObject = new FadeTransition(this);
                    break;
                case 'slide':
                    this._transitionObject = new SlideTransition(this);
                    break;
                case 'smooth':
                    this._transitionObject = new SmoothTransition(this);
                    break;
                default:
                    throw new Error('No transition defined. Transition specified: ' + transition);
            }
        },




        config: function(name, value, performValidation) {
            // no value was passed in -- return current value
            if (value === undefined) {
                return this._carouselConfiguration.getValue(name);
            }

            if (performValidation === undefined) {
                performValidation = true;
            }

            // a value was passed in, trigger setting of this value
            var returnValue = this._carouselConfiguration.setValue(name, value);

            // validate if desired
            if (performValidation) {
                this._carouselConfiguration.validate();
            }

            return returnValue;
        },

        state: function(name, value) {

            // no value was passed in -- return current value
            if (value === undefined) {
                return this._state[name];
            }

            this._state[name] = value;
        },










        /**
         * Getters and Setters
         */

        getCurrentSlideNumber: function() {
            return this.state('currentSlideNumber');
        },

        getNumberOfSlides: function() {
            return this._numberOfSlides;
        },

        getSlide: function(slideNumber) {
            return this.getAllSlides().eq(slideNumber);
        },

        getAllSlides: function() {
            return this.getDOMReference('carouselList').find('.carousel-item');
        },

















        disableCarousel: function() {
            this.state('disableCarousel', true);
        },

        enableCarousel: function() {
            this.state('disableCarousel', false);
        },

        resetCurrentSlide: function() {
			// if the reset function gets called prior to the carousel being 
			// (IE8, more?) fully initialized, we have no need to reset the slide
			if (!this.state('carouselInitialized')) {
				return;
			}
            this.moveToSlide(this.state('currentSlideNumber'), null, true);
        },

        /**
         * Moves to a slide based on a 0 index reference pattern
         */
        moveToSlide: function(currentSlideNumber, options, bypassSanityCheck) {

            if (bypassSanityCheck) {
                this._transitionObject.triggerTransition(currentSlideNumber, options);

                // update the current slide number taking the total number of slides into account
                this.state('currentSlideNumber', currentSlideNumber % this._numberOfSlides);

                return;
            }

            if (this.state('disableCarousel') == true) {
                return;
            }

            // if we're already on the slide we're trying to navigate to, return
            if (currentSlideNumber == this.state('currentSlideNumber')) {
                return;
            }

            // disallow changing of navigation during animation where appropriate
            if (this.config('disableControlsOnChange') && this.state('changingSlide')) {
                return;
            }

            // handle arguments not passed in
            if (options === undefined) {
                options = {};
            }

            if (options.stopAutoPlay == null) {
                options.stopAutoPlay = false;
            }

            if (options.scrollSpeed == null) {
                options.scrollSpeed = this.config('scrollSpeed');
            }
            
            if (options.fadeTransitionSpeed == null) {
                options.fadeTransitionSpeed = this.config('fadeTransitionSpeed');
            }

            if (options.directionReversed == null) {
                options.directionReversed = false;
            }

            if (options.stopAutoPlay) {
                this.stopAutoPlay();
            }

            // store the previous slide for later use
            var previousSlideNumber = this.state('currentSlideNumber');

            this.updateAutoPlayProgress(0);

            // make aware that we're changing slides
            this.toggleChangingSlide(true);

            // call the transition via the stored object
            this._transitionObject.triggerTransition(currentSlideNumber, options);

            // update the current slide number taking the total number of slides into account
            this.state('currentSlideNumber', currentSlideNumber % this._numberOfSlides);

            this.updateNavigation();
            this.updateIndicators();

            this._triggerSlideChangeEvents(previousSlideNumber, options.relativeOffset);

            this.state('previousAutoPlaySlideChangeTime', new Date().getTime());
        },

        _triggerSlideChangeEvents: function(previousSlideNumber, relativeOffset) {

            if (previousSlideNumber === undefined) {
                previousSlideNumber = 0;
            }

            if (relativeOffset === undefined) {
                relativeOffset = 0;
            }

            // call any events set to be run on slide change
            if (this._onSlideChangeEvents && typeof this._onSlideChangeEvents == 'object') {

                var onChangeEventData = {
                    previousSlideNumber: previousSlideNumber,
                    currentSlideNumber: this.state('currentSlideNumber'),
                    actualSlideNumber: this.state('actualSlideNumber'),
                    relativeOffset: relativeOffset || null,
                    numberOfSlides: this._numberOfSlides,
                    slideOffset: this.state('slideOffset')
                };

                for (var i = 0; i < this._onSlideChangeEvents.length; i++) {
                    if (typeof this._onSlideChangeEvents[i] == 'function') {
                        // call the event passing in appropriate data
                        this._onSlideChangeEvents[i](onChangeEventData);
                    }
                }
            }
        },

        moveRelativeToSlide: function(offset, stopAutoPlay) {
            if (stopAutoPlay === undefined) {
                stopAutoPlay = true;
            }

            var options = {}
            options.directionReversed = (offset < 0);
            options.relativeOffset = offset;

            // NOTE: This works as desired (though mathematically incorrect)
            // due to the javascript modulus bug
            var newSlide = (this.state('currentSlideNumber') + offset) % this._numberOfSlides;

            if (newSlide < 0) {
                newSlide += this._numberOfSlides;
            }
            
            if (this.config('allowWrapping') == false && ((newSlide < this.state('currentSlideNumber') && offset > 0) || (newSlide > this.state('currentSlideNumber') && offset < 0))) {
                return
            }

            this.moveToSlide(newSlide, options);
        },

        disableAutoPlay: function() {
            this.stopAutoPlay();
            this.state('disableAutoPlay', true);
        },

        enableAutoPlay: function() {
            this.state('disableAutoPlay', false);
        },

        // TODO: move this
        _onAutoPlayIntervalDelayReached: function() {

            var currentTime = (new Date()).getTime();

            // if we're currently changing the slide, no need to continue further
            if (this.state('changingSlide')) {
                this.state('previousAutoPlaySlideChangeTime', currentTime);
                return;
            }

            var timeElapsed = currentTime - this.state('previousAutoPlaySlideChangeTime');

            // check progress, update autoplay progress, and change slide if appropriate
            if (timeElapsed >= this.config('autoPlayDelay')) {
                this.updateAutoPlayProgress(1);
                this.moveRelativeToSlide(this.config('autoPlayStep'), false);
            } else {
                this.updateAutoPlayProgress(timeElapsed / this.config('autoPlayDelay'));
            }
        },

        startAutoPlay: function() {
            if (this.state('disableAutoPlay')) {
                return;
            }

            this.state('previousAutoPlaySlideChangeTime', (new Date()).getTime());

            this.state('autoPlayInterval', setInterval(
                this._onAutoPlayIntervalDelayReached.bind(this), 
                1000 / this._autoPlayProgressFPS
            ));
        },

        updateAutoPlayProgress: function(percent) {
            // update progress functions
            if (this._autoPlayProgressEvents && typeof this._autoPlayProgressEvents == 'object') {

                var autoPlayProgressEventData = {
                    percent: percent
                };

                for (var i = 0; i < this._autoPlayProgressEvents.length; i++) {
                    if (typeof this._autoPlayProgressEvents[i] == 'function') {
                        // call the event passing in appropriate data
                        this._autoPlayProgressEvents[i](autoPlayProgressEventData);
                    }
                }
            }
        },

        stopAutoPlay: function() {
            clearInterval(this.state('autoPlayInterval'));
            this.state('autoPlayInterval', null);
        },

        updateNavigation: function() {
            // update navigation if available
            if (this.getDOMReference('carouselNav').size() > 0) {
                var $navSlides = this.getDOMReference('carouselNav').children().eq(0).children();
                
                

                $navSlides.removeClass('carousel-nav-item-active');
                
                jQuery($navSlides.get(this.state('currentSlideNumber')))
                    .addClass('carousel-nav-item-active');
                    
            }
        },

        changeSlide: function(slideNumber, updateCurrentSlide, options) {
            
            if (options == null) {
                options = {};
            }

            var animateParams = {};

            var positionData = this.getPositioningData(slideNumber);
            animateParams[positionData.property] = positionData.position;

            var onSlideChangeComplete = (options.preventSlideChangeCompleteEvent)
                ? null
                : this._onChangeSlideComplete.bind(this, options);

            this.getDOMReference('carouselList')
                .stop()
                .animate(
                    animateParams, 
                    options.scrollSpeed || 0, 
                    onSlideChangeComplete
                );

            // update the actual slide number regardless of whether or not we're updating the update current slide var
            this.state('actualSlideNumber', slideNumber);

            if (updateCurrentSlide) {
                this.state('currentSlideNumber', slideNumber);
            }
        },

        _onChangeSlideComplete: function(options) {
            this.slideChangeComplete();
        },

        slideChangeComplete: function(options) {

            if (options == null) {
                options = {};
            }

            // done changing slides
            this.toggleChangingSlide(false);

            var onComplete = options.onComplete;

            if (onComplete != null && typeof onComplete == 'function') {
                onComplete();
            }
        },

        getPositioningData: function(slideNumber) {
            var returnData = {
                property: null,
                position: null
            }

            if (this.config('direction') == 'vertical') {
                // vertical specific params
                var topPos = (this._carouselReversed) 
                    ? -1 * (this._slideSize.height * (this._virtualNumberOfSlides - slideNumber - 1))
                    : -1 * this._slideSize.height * slideNumber;
                
                returnData.property = 'top';
                returnData.position = topPos;
            } else {
                // horizontal specific params
                var leftPos = (this._carouselReversed) 
                    ? -1 * (this._slideSize.width * (this._virtualNumberOfSlides - slideNumber))
                    : -1 * this._slideSize.width * slideNumber;

                returnData.property = 'left';
                returnData.position = leftPos;
            }

            return returnData;
        },

        toggleChangingSlide: function(newState) {

            if (newState === undefined) {
                newState = !this.state('changingSlide');
            }

            if (newState === true) {
                this.state('changingSlide', true);
                
                if (this.config('disableControlsOnChange') && this.getDOMReference('carouselNav')) {
                    this.getDOMReference('carouselWrapper').addClass('carousel-navigation-disabled');
                }
            } else {
                this.state('changingSlide', false);

                if (this.config('disableControlsOnChange') && this.getDOMReference('carouselNav')) {
                    this.getDOMReference('carouselWrapper').removeClass('carousel-navigation-disabled');
                }
            }
        },

        fullSlideIsVisible: function($slide) {

            var $list = $slide.parent();

            if (this.config('direction') == 'horizontal') {
                var listLeftVisible = -1 * $list.position().left;
                var listRightVisible = listLeftVisible + $list.parent().outerWidth();

                var slideLeft = $slide.position().left;
                var slideRight = slideLeft + $slide.outerWidth();

                if (!(slideLeft >= listLeftVisible && slideRight <= listRightVisible)) {
                    return {
                        left: slideLeft - listLeftVisible,
                        right: listRightVisible - slideRight
                    }
                }
            } else if (this.config('direction') == 'vertical') {
                // TODO: this code is untested
                var listTopVisible = -1 * $list.position().top;
                var listBottomVisible = listTopVisible + $list.parent().outerHeight();

                var slideTop = $slide.position().top;
                var slideBottom = slideTop + $slide.outerHeight();

                if (!(slideTop >= listTopVisible && slideBottom <= listBottomVisible)) {
                    return {
                        top: slideTop - listTopVisible,
                        bottom: listBottomVisible - slideBottom
                    }
                }
            }
            
            return true;
        },

        updateIndicators: function() {
            var currentSlideNumber = this.state('actualSlideNumber');

            this.getDOMReference('carouselWrapper').find('.carousel-slide-number').html((currentSlideNumber + 1));
            this.getDOMReference('carouselWrapper').find('.carousel-total-slides').html(this._numberOfSlides);

            // Add slide classes
            this.getDOMReference('carouselList').children('li').removeClass('carousel-prev-indicator carousel-current-indicator carousel-next-indicator');
            this.getDOMReference('carouselList').children('li').eq(currentSlideNumber).addClass('carousel-current-indicator');
            this.getDOMReference('carouselList').children('li').eq(currentSlideNumber).next().addClass('carousel-next-indicator');
            this.getDOMReference('carouselList').children('li').eq(currentSlideNumber).prev().addClass('carousel-prev-indicator');

            // update previous/next navigation buttons
            var numberOfSlides = this.getNumberOfSlides();

            if (numberOfSlides < 2) {
                this._setPreviousSlideButtonEnabledStatus(false);
                this._setNextSlideButtonEnabledStatus(false);
            } else if (!this.config('allowWrapping')) {
                var currentSlideNumber = this.state('actualSlideNumber');

                if (currentSlideNumber == 0 || currentSlideNumber == undefined) {
                    this._setPreviousSlideButtonEnabledStatus(false);
                    this._setNextSlideButtonEnabledStatus(true);
                } else if (currentSlideNumber == numberOfSlides - 1) {
                    this._setPreviousSlideButtonEnabledStatus(true);
                    this._setNextSlideButtonEnabledStatus(false);
                } else {
                    this._setPreviousSlideButtonEnabledStatus(true);
                    this._setNextSlideButtonEnabledStatus(true);
                }
            }
        },

        _setPreviousSlideButtonEnabledStatus: function(enabled) {
            var $navigationButton = this.getDOMReference('carouselWrapper').find('.js-carousel-previous-slide');
            this._setNavigationButtonEnabledStatus($navigationButton, enabled);
        },

        _setNextSlideButtonEnabledStatus: function(enabled) {
            var $navigationButton = this.getDOMReference('carouselWrapper').find('.js-carousel-next-slide');
            this._setNavigationButtonEnabledStatus($navigationButton, enabled);
        },

        _setNavigationButtonEnabledStatus: function($navigationButton, enabled) {
            if (enabled) {
                $navigationButton.removeClass('disabled');
            } else {
                $navigationButton.addClass('disabled');
            }
        },

        // externalize commands in a fluent interface
        command: function(args) {

            if (args == undefined) {
                return false;
            }

            var command = args[0];
            if (typeof command == 'string') {
                switch (command) {
                    case 'startAutoPlay':
                        this.startAutoPlay();
                        return;

                    case 'stopAutoPlay':
                        this.stopAutoPlay();
                        return;

                    case 'moveRelativeToSlide':
                        var move = 1;
                        if (typeof args[1] == 'number') {
                            move = args[1];
                        }

                        this.moveRelativeToSlide(move, args[2]);
                        return;

                    case 'moveToSlide':
                        if (typeof args[1] == 'number') {
                            this.moveToSlide(args[1]);
                        }
                        return;

                    case 'disableCarousel':
                        this.disableCarousel();
                        return;

                    case 'enableCarousel':
                        this.enableCarousel();
                        return;

                    case 'config':
                        this.config(args[1], args[2]);
                        this._carouselConfiguration.validate();
                        break;

                    case 'reinitialize':
                        this._reinitializeCarousel();
                        return;
                }
            }
        }
    };

    // add the plugin to jQuery
    jQuery.fn.NCarousel = function() {
        var params = arguments[0];
        var args = arguments;

        return this.each(function(i, ele) {
            var $ele = jQuery(ele);
            var eleDataNCarousel = $ele.data('NCarousel');

            if (eleDataNCarousel != undefined && eleDataNCarousel instanceof NCarousel) {
                eleDataNCarousel.command(args);
            } else {
                new NCarousel(jQuery(this), params);
            }
        })
    };

    return NCarousel;

});
