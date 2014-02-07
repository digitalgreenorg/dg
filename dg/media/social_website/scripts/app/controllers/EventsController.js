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
    
    require('libs/external/swfobject/swfobject');
    var registrationFormTemplate = require('text!app/views/events/registration-form.html');

    var EventsController = DigitalGreenPageController.extend({

        /**
         * Controller constructor
         * @return {EventsController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            


            var references = this._references;
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
            
            // play button 
            references.$playButton = jQuery('.play-button');
            
            //register button
            references.$registerButton = jQuery('.js-register-button');
        },
        
        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;
            
            boundFunctions.onPlayButtonClick = this._onVideoPlayButtonClick.bind(this);
            references.$playButton.on('click', boundFunctions.onPlayButtonClick);
            
            boundFunctions.onRegisterButtonClick = this._onRegisterButtonClick.bind(this);
            references.$registerButton.on('click', boundFunctions.onRegisterButtonClick);
        },
        
        _onRegisterButtonClick: function () {
            // Add a the Registration section
            $("#registration").remove();
            this._references.$registerButton.closest('section.about-bg').after(registrationFormTemplate);
            var body = jQuery("html, body");
            body.animate({ scrollTop: $('#registration').offset().top }, 1000);
            
            // Add click handlers to form-tabs
            this._references.$registration_form_tabs = jQuery(".js-form-tab");
            var boundFunctions = this._boundFunctions;
            boundFunctions.onFormTabClick = this._onFormTabClick.bind(this);
            this._references.$registration_form_tabs.on('click', boundFunctions.onFormTabClick);
        },
        
        _onFormTabClick: function (event) {
            event.preventDefault();
            var form_tab = jQuery(event.target);
            var form_tabs = this._references.$registration_form_tabs;
            form_tabs.removeClass('active');
            form_tab.addClass('active');
            var index = form_tabs.index(form_tab);
            var forms = jQuery('.js-form');
            forms.addClass('hide');
            jQuery(forms[index]).removeClass('hide');
        },
        
        _initVideoPlayer: function() {

            var videoId = 'CR8zRC3wd-s';

            var params = { allowScriptAccess: "always" };
            var atts = { id: "player", 
       			 		 class: 'main-carousel-video-player'
		    			};
            
            swfobject.embedSWF(
                'http://www.youtube.com/v/' + videoId + '?enablejsapi=1&playerapiid=ytplayer&version=3',
                'player',
                '1024',
                '424',
                '8',
                null,
                null,
                params,
                atts
            );

            window.onYouTubePlayerReady = this._onYouTubePlayerReady.bind(this);
            $("#video-img > div").not("#player").each(function(index, ele){$(ele).hide();});
            $("#player").show();
        },

        _onYouTubePlayerReady: function() {
            // clean up the window
            window.onYouTubePlayerReady = undefined;

            var videoPlayer = jQuery('#player').get(0);
            this._references.videoPlayer = videoPlayer;

            // youtube seems to force us to put functions in the window
            // we'll do our best to handle that elegantly
            window.onYouTubePlayerStateChange = this._onYouTubePlayerStateChange.bind(this);

            videoPlayer.addEventListener('onStateChange', 'onYouTubePlayerStateChange');
            
            videoPlayer.playVideo();
            
        },

        _onYouTubePlayerStateChange: function(newState) {
            if (newState == 0){
            	$("#player").hide();          
            	$("#video-img > div").not("#player").each(function(index, ele){$(ele).show();});
            }
        	
        },
        
        _onVideoPlayButtonClick: function(e) {
        	this._initVideoPlayer();
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return EventsController;
});
