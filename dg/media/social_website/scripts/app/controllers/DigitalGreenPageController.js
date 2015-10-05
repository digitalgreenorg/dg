/**
 * DigitalGreenPageController Class File
 *
 * @author rdeluca
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';

    var PageController = require('framework/controllers/PageController');
    var globalEventManager = require('framework/globalEventManager');
    var Util = require('framework/Util');
    var jQuery = require('jquery');

    var CustomSelectBox = require('app/libs/CustomSelectBox');

    var SearchViewController = require('app/view-controllers/SearchViewController');
    

    var DigitalGreenPageController = PageController.extend({

        /**
         * Controller constructor
         * @return {DigitalGreenPageController} this
         */
        constructor: function(bootstrapConfig, globalHelpers) {
            this.base(bootstrapConfig, globalHelpers);

            var languageCookie = Util.Cookie.get('language__name');

            var $customSelectElement = jQuery('.js-custom-select');
            if ($customSelectElement.length) {
                var languageSelectBox = new CustomSelectBox($customSelectElement);

                // rebroadcast the optionChanged event to alert that the language has changed
                languageSelectBox.on('optionChanged', this._onOptionChanged.bind(this));

                languageSelectBox.setOption(languageCookie);
            } else {
                // on pages with no select box, we have to manually trigger the language changed event
                // on initial load to get the information out
                //globalEventManager.trigger('languageChanged', languageCookie);
            }
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base($referenceBase);

            var references = this._references;
            
            references.$userImage = jQuery('.js-user-image');
            references.$userDropDown = jQuery('.js-user-dropdown');
            references.$userDropDownArrow = jQuery('.js-user-dropdown-arrow');
            
            // helpers
            var $searchContainer = jQuery(".js-search-wrapper");
            references.searchViewController = new SearchViewController($searchContainer);

            //survey
            references.$feedbackModal = jQuery(".js-modal");
            references.$smileyClick = jQuery(".js-smiley-click")
            references.$submitForm = jQuery(".js-submit-form")
        },
        
        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onUserImageClick = this._onUserImageClick.bind(this);
            references.$userImage.on('click', boundFunctions.onUserImageClick);

            boundFunctions.onSmileyClick = this._onSmileyClick.bind(this);
            references.$smileyClick.on('click', boundFunctions.onSmileyClick);

            boundFunctions.onSubmitClick = this._onSubmitClick.bind(this);
            references.$submitForm.on('click', boundFunctions.onSubmitClick);
        },

        _onOptionChanged: function(value) {
            Util.Cookie.set('language__name', value);
            globalEventManager.trigger('languageChanged', value);
        },

        _onUserImageClick: function(e) {
            e.preventDefault();
            this._references.$userDropDown.toggle();
            this._references.$userDropDownArrow.toggle();
            $('html, body').animate({scrollTop:0}, 'slow');
        },

        _onSmileyClick: function(e){
            e.preventDefault();
            $(".selected").removeClass("selected");
            var a = $(e.currentTarget);
            a.addClass("selected");
            this._references.$feedbackModal.removeClass("comment-survey");
        },

        _onSubmitClick: function(){
            var comments = $("#comments").val();
            var email = $("#email").val();
            var csrf_token = $("#csrftoken").val();
            var a = $(".selected");
            var rating = a.attr("data");
            $.ajax({
                url : "/feedbacksubmit_json", 
                type : "POST",
                dataType: "json", 
                data : {
                    comments: comments,
                    email: email,
                    rating: rating
                    },
                success : function(json) {
                    location.href="#close";
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
                    location.href="#close";
                }
            });
            return false;
        },

        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();
        }
    });

    return DigitalGreenPageController;
});
