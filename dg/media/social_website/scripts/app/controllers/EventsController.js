/**
 * EventsController Class File
 *
 * @author nandini
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var jQuery = require('jquery');

    var NCarousel = require('libs/NCarousel/NCarousel');
    var notify = require('libs/external/notify.min')
    
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
            
            references.$registerSection = jQuery("#registration");
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
            // Remove and add the Registration section
            /* TODO Adjust about-bg-white sequence */
            this._references.$registerSection.remove();
            this._references.$registerButton.closest('section.about-bg').after(registrationFormTemplate);
            
            this._references.$registrationFormTabs = jQuery(".js-form-tab");
            this._references.$registerSubmitButtons = jQuery('.js-submit-registration');
            
            this._references.$csrfToken = this._references.$registerButton.attr('data-csrf-input');
            
            var boundFunctions = this._boundFunctions;
            
            // Add click handlers to form-tabs
            boundFunctions.onFormTabClick = this._onFormTabClick.bind(this);
            this._references.$registrationFormTabs.on('click', boundFunctions.onFormTabClick);
            
            // Add click handlers to form submit buttons
            boundFunctions.onSubmitRegistrationButtonClick = this._onSubmitRegistrationButtonClick.bind(this);
            this._references.$registerSubmitButtons.on('click', boundFunctions.onSubmitRegistrationButtonClick);
            
            // Scroll to Registration section
            var body = jQuery("html, body");
            body.animate({ scrollTop: $('#registration').offset().top }, 1000);
        },
        
        _onSubmitRegistrationButtonClick: function (event) {
            event.preventDefault();
            var $submitButton = jQuery(event.target);
            var $form = $submitButton.closest('form');
            var $formResult = $form.find('.js-form-result');
            var $inputsRequired = $form.find('.js-required');
            var $inputsEmail = $form.find('.js-email')
            
            $formResult.html("");
            $form.append(this._references.$csrfToken);
            
            /* Validate fields
             * Check that email not empty and matches Regular Expression
             * Check that name, organization not empty
            */
            var error_messages = "";
            $inputsRequired.each(function(){
                if (this.value == "") {
                    $(this).notify("This Field is required. It cannot be left blank.");
                    error_messages += $(this).attr("name") + " is required. It cannot be left blank.<br/>";
                }
            });
            $inputsEmail.each(function(){
                var email = this.value;
                /* The world's greatest regular expression */
                var emailRegExp = new RegExp(/^(("[\w-\s]+")|([\w-]+(?:\.[\w-]+)*)|("[\w-\s]+")([\w-]+(?:\.[\w-]+)*))(@((?:[\w-]+\.)*\w[\w-]{0,66})\.([a-z]{2,6}(?:\.[a-z]{2})?)$)|(@\[?((25[0-5]\.|2[0-4][0-9]\.|1[0-9]{2}\.|[0-9]{1,2}\.))((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\.){2}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[0-9]{1,2})\]?$)/i);
                var valid = emailRegExp.test(email);
                if (!valid) {
                    $(this).notify("This is not a valid email");
                    error_messages += $(this).attr("name") + " is not a valid email.<br/>";
                }
            });
            if (error_messages!="") {
                //$formResult.append(error_messages);
                return;
            }
            
            var formQueryString = $form.serialize();
            jQuery.ajax
            ({
                type: "POST",
                url: "registration/",
                data: formQueryString,
                cache: false,
                success: function(message)
                {
                    $formResult.append(message);
                }
            });
        },
        
        _onFormTabClick: function (event) {
            event.preventDefault();
            var form_tab = jQuery(event.target);
            var form_tabs = this._references.$registrationFormTabs;
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
