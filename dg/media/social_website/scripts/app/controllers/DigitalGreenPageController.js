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
            references.$smileyClick = jQuery(".js-smiley-click");
            references.$submitForm = jQuery(".js-submit-form");
            references.$modalClick = jQuery(".js-modal-click");
        },
        
        _initEvents: function() {
            this.base();
            
            var references = this._references;
            var boundFunctions = this._boundFunctions;

            boundFunctions.onUserImageClick = this._onUserImageClick.bind(this);
            references.$userImage.on('click', boundFunctions.onUserImageClick);

            boundFunctions.onModalClick = this._onModalClick.bind(this);
            references.$modalClick.on('click', boundFunctions.onModalClick);

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

        _onModalClick: function(e){
            $(".js-modal").addClass("comment-survey");
            $('#comments').val('');
            $('#email').val('');
            $(".icon-selected").removeClass("icon-selected");
        },

        _onSmileyClick: function(e){
            e.preventDefault();
            $(".icon-selected").removeClass("icon-selected");
            var a = $(e.currentTarget);
            a.addClass("icon-selected");
            this._references.$feedbackModal.removeClass("comment-survey");
        },

        _onSubmitClick: function(){
            var comments = $("#comments").val();
            var email = $("#email").val();
            var csrf_token = $("#csrftoken").val();
            var a = $(".icon-selected");
            var rating = a.attr("data");
            location.href="#close";
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
                },
                error : function(xhr,errmsg,err) {
                    alert(xhr.status + ": " + xhr.responseText);
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
