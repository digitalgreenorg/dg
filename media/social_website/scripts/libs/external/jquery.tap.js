(function(document, $) {
    'use strict';

    /**
     * Flag to determine if touch is supported
     *
     * @type {Boolean}
     * @constant
     */
    $.support.touch = (('ontouchstart' in window) || window.DocumentTouch && document instanceof DocumentTouch);

    /**
     * Max tap duration
     *
     * @type {Number}
     * @constant
     */
    var MAX_DURATION = 300;

    /**
     * Max touch move
     *
     * @type {Number}
     * @constant
     */
    var MAX_MOVE = 10;

    /**
     * Event namespace
     *
     * @type {String}
     * @constant
     */
    var HELPER_NAMESPACE = '.__tap-helper';

    /**
     * Event name
     *
     * @type {String}
     * @constant
     */
    var EVENT_NAME = 'tap';

    /**
     * Unique ID used to generate unique helper namespaces
     *
     * @type {Number}
     * @static
     */
    var ID = 0;

    /**
     * Event variables to copy to touches
     *
     * @type {Array}
     * @constant
     */
    var EVENT_VARIABLES = [
        'clientX',
        'clientY',
        'screenX',
        'screenY',
        'pageX',
        'pageY'
    ];

    /**
     * Create tap event with data from touchEnd event
     *
     * @param {Event} e
     * @param {Object} data
     * @return {jQuery.Event}
     * @private
     */
    var _createTapEvent = function(e, data) {
        var i = 0;
        var length = EVENT_VARIABLES.length;
        var touch = e.originalEvent.changedTouches[0];

        var event = $.Event(EVENT_NAME, e);
        event.type = EVENT_NAME;
        event.data = data;

        for (; i < length; i++) {
            event[EVENT_VARIABLES[i]] = touch[EVENT_VARIABLES[i]];
        }

        return event;
    };

    /**
     * Tap Class that will you touch/click events to trigger a tap event
     * @class
     * @name Tap
     *
     * @param {jQuery} $target
     * @param {Object} handleObj
     * @constructor
     */
    function Tap($target, handleObj) {

        /**
         * Target element
         *
         * @name Tap#$target
         * @type {jQuery}
         */
        this.$target = $target;

        /**
         * Event selector
         *
         * @name Tap#selector
         * @type {String}
         */
        this.selector = handleObj.selector;

        /**
         * Data to pass to event trigger
         *
         * @name Tap#data
         * @type {Object}
         */
        this.data = handleObj.data;

        /**
         * Has touch moved past threshold?
         *
         * @name Tap#moved
         * @type {Boolean}
         */
        this.moved = false;

        /**
         * Helper events namespace
         *
         * @name Tap#namespace
         * @type {Number}
         */
        this.namespace = HELPER_NAMESPACE + (ID++);

        /**
         * X position of touch on touchstart
         *
         * @name Tap#startX
         * @type {Number}
         */
        this.startX = 0;

        /**
         * Y position of touch on touchstart
         *
         * @name Tap#startY
         * @type {Number}
         */
        this.startY = 0;

        /**
         * time of touch on touchstart
         *
         * @name Tap#startTime
         * @type {Number}
         */
        this.startTime = 0;

        /**
         * Number of touches
         *
         * @name Tap#touchStartCount
         * @type {Number}
         */
        this.touchStartCount = 0;

        this
            .setupHandlers()
            .reset()
            .enable();
    }

    Tap.prototype = {

        /**
         * Setup event handlers
         *
         * @return {Tap}
         */
        setupHandlers: function() {

            /**
             * _onTouchStart handler
             *
             * @name Tap#onTouchStart
             * @type {Function}
             */
            this.onTouchStart = this._onTouchStart.bind(this);

            /**
             * _onTouchMove handler
             *
             * @name Tap#onTouchMove
             * @type {Function}
             */
            this.onTouchMove = this._onTouchMove.bind(this);

            /**
             * _onTouchEnd handler
             *
             * @name Tap#onTouchEnd
             * @type {Function}
             */
            this.onTouchEnd = this._onTouchEnd.bind(this);

            /**
             * _onTouchCancel handler
             *
             * @name Tap#onTouchCancel
             * @type {Function}
             */
            this.onTouchCancel = this._onTouchCancel.bind(this);

            /**
             * _onClick handler
             *
             * @name Tap#onClick
             * @type {Function}
             */
            this.onClick = this._onClick.bind(this);

            return this;
        },

        /**
         * Start listening for touchstart
         *
         * @return {Tap}
         */
        enable: function() {
            if ($.support.touch) {
                this.$target.on('touchstart' + this.namespace, this.selector, this.onTouchStart);
            } else {
                this.$target.on('click' + this.namespace, this.selector, this.onClick);
            }
            return this;
        },

        /**
         * Stop listening for touchstart
         *
         * @return {Tap}
         */
        disable: function() {
            if ($.support.touch) {
                this.$target.off('touchstart' + this.namespace, this.selector, this.onTouchStart);
            } else {
                this.$target.off('click' + this.namespace, this.selector, this.onClick);
            }
            return this;
        },

        /**
         * Reset values
         *
         * @return {Tap}
         */
        reset: function() {
            //reset state
            this.moved = false;
            this.startX = 0;
            this.startY = 0;
            this.startTime = 0;
            this.touchStartCount = 0;

            return this;
        },

        /**
         * Destroy Tap object
         *
         * @return {Tap}
         */
        destroy: function() {
            this.onTouchCancel();
            return this.disable();
        },

        /**
         * Save touch position and start listening to touchmove and touchend
         *
         * @param {jQuery.Event} e
         * @private
         */
        _onTouchStart: function (e) {
            this.touchStartCount = e.originalEvent.touches.length;

            if (this.touchStartCount > 1) {
                return;
            }

            /**
             * Target element
             *
             * @name Tap#$element
             * @type {HTMLElement}
             */
            this.$element = $(e.target);

            this.moved = false;
            this.startX = e.originalEvent.touches[0].clientX;
            this.startY = e.originalEvent.touches[0].clientY;
            this.startTime = Date.now();

            this.$target
                .on('touchmove' + this.namespace, this.selector, this.onTouchMove)
                .on('touchend' + this.namespace, this.selector, this.onTouchEnd)
                .on('touchcancel' + this.namespace, this.selector, this.onTouchCancel);
        },

        /**
         * Determine if touch has moved too far to be considered a tap
         *
         * @param {jQuery.Event} e
         * @private
         */
        _onTouchMove: function (e) {
            var x = e.originalEvent.touches[0].clientX;
            var y = e.originalEvent.touches[0].clientY;

            //if finger moves more than 10px flag to cancel
            if (Math.abs(x - this.startX) > MAX_MOVE || Math.abs(y - this.startY) > MAX_MOVE) {
                this.moved = true;
            }
        },

        /**
         * Determine if a valid tap event and trigger tap
         *
         * @param {jQuery.Event} e
         * @private
         */
        _onTouchEnd: function (e) {
            if (!this.touchStartCount || e.originalEvent.touches.length > 0) {
                return;
            }

            if (this.touchStartCount > 1) {
                return;
            }

            var targetTag = e.target.tagName;

            var preventDefaultInteraction = (e.target == e.currentTarget || (targetTag != 'A'));

            // TODO: DEBUG THIS FURTHER (tapping on the button on mobile doesn't trigger the event in some cases when all of these output true)
            // console.log('1' + !e.originalEvent.firstTap);
            // console.log('2' + !this.moved);
            // console.log('3' + (Date.now() - this.startTime < MAX_DURATION));
            // console.log('4' + preventDefaultInteraction);

            if (!e.originalEvent.firstTap && !this.moved && Date.now() - this.startTime < MAX_DURATION && preventDefaultInteraction) {
                // Make sure any parents also emulating a tap event do not also fire tap.
                // Triggering the event below will bubble the event anyway.
                e.originalEvent.firstTap = true;
                this.$target.trigger(_createTapEvent(e, this.data));
            }

            this.onTouchCancel();
        },

        /**
         * Remove touchmove, touchend, and touchcancel events
         *
         * @private
         */
        _onTouchCancel: function () {
            this
                .reset()
                .$target
                .off('touchmove' + this.namespace, this.selector, this.onTouchMove)
                .off('touchend' + this.namespace, this.selector, this.onTouchEnd)
                .off('touchcancel' + this.namespace, this.selector, this.onTouchCancel);
        },

        /**
         * If this is not a manual jQuery.trigger, then trigger the tap event for desktop clicks
         *
         * @private
         */
        _onClick: function(e) {
            if (!e.isTrigger && !e.originalEvent.firstTap) {
                // Make sure any parents also emulating a tap event do not also fire tap.
                // Triggering the event below will bubble the event anyway.
                e.originalEvent.firstTap = true;
                e.type = 'tap';
                this.$target.trigger(e);
            }
        }
    };

    /**
     * Create new special tap event
     *
     * @type {Object}
     */
    $.event.special[EVENT_NAME] = {

        /**
         * Create new tap object and bind touchstart event
         *
         * @param {Object} handleObj
         */
        add: function(handleObj) {
            handleObj.tap = new Tap($(this), handleObj);
        },

        /**
         * Remove all Tap events
         *
         * @param {Object} handleObj
         */
        remove: function(handleObj) {
            if (handleObj.tap && handleObj.tap.destroy) {
                handleObj.tap.destroy();
            }
        }
    };

}(document, jQuery));