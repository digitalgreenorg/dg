/**
 * CollectionAddEditController Class File
 *
 * @author aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';
    var DigitalGreenPageController = require('app/controllers/DigitalGreenPageController');
    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var jQuery = require('jquery');
    var CollectionDropDownDataFeed = require('app/libs/CollectionDropDownDataFeed');
    var collectionDropDownTemplate = require('text!app/views/collection-add-dropdown.html');
    var CollectionVideoDropDownDataFeed = require('app/libs/CollectionVideoDropDownDataFeed');
    var collectionVideoDropDownTemplate = require('text!app/views/collection-add-video-dropdown.html');
    var carouselTemplate = require('text!app/views/collection-add-video-carousel.html');
    var Chosen = require('libs/external/chosen.jquery.min');
    
    var CollectionDropDownController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);
            
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();
            var references = this._references;
            references.dataFeed = new CollectionDropDownDataFeed();
            references.videodataFeed = new CollectionVideoDropDownDataFeed();
            references.$collectionAddWrapper = $referenceBase;
            references.$collectionDropDownContainer = $referenceBase.find('.js-collection-dropdown-container');
        },

        _initEvents: function() {
            this.base();
            this.getCollectionDropDown();
            var boundFunctions = this._boundFunctions;
            var references = this._references;
            
            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);
            
            boundFunctions.onVideoDataProcessed = this._onVideoDataProcessed.bind(this);
            references.videodataFeed.on('dataProcessed', boundFunctions.onVideoDataProcessed);
            
        },
        
        getCollectionDropDown: function() {
            var collectiondropdownData = this._references.dataFeed.getCollectionDropDown();
            if (collectiondropdownData == false) {
                return false;
            }
            this._renderCollectionDropDown(collectiondropdownData);
            this._boundFunctions.onDropDownChosen = this._onDropDownChosen.bind(this);
            $(".js-dropdown").on('change', this._boundFunctions.onDropDownChosen);
        },

        getCollectionVideoDropDown: function() {
        	var collectionvideodropdownData = this._references.videodataFeed.getCollectionVideoDropDown();
            if (collectionvideodropdownData == false) {
                return false;
            }
            this._references.videoarray = collectionvideodropdownData;
            this._renderVideoCollectionDropDown(collectionvideodropdownData);
            this._boundFunctions.onVideoChosen = this._onVideoChosen.bind(this);
            $("#vidlist").on('change', this._boundFunctions.onVideoChosen);
            
        },
        _onDataProcessed: function() {
            this.getCollectionDropDown();
        },
        
        _onVideoDataProcessed: function() {
        	this.getCollectionVideoDropDown();
        },

        _renderCollectionDropDown: function(collectiondropdownData) {
            var renderedCollectionDropDown = viewRenderer.render(collectionDropDownTemplate, collectiondropdownData);
            this._references.$collectionDropDownContainer.html(renderedCollectionDropDown);
            this._dropdownChosen();
        },
        
        _renderVideoCollectionDropDown: function(collectionvideodropdownData) {
        	 var renderData = {
                     video: collectionvideodropdownData
                 };
            var renderedCollectionVideoDropDown = viewRenderer.render(collectionVideoDropDownTemplate, renderData);
            $('.js-collection-video-dropdown-container').html(renderedCollectionVideoDropDown);
            this._dropdownChosen();
        },

        _dropdownChosen: function(){
        	var references = this._references;
            $(".chosen-select").chosen({no_results_text: "No results match", width: "90%"});
        },
        
        _onDropDownChosen: function(){
        	var references = this._references;
        	if( $("#partnerlist").val()!="" && $("#statelist").val()!="" && $("#langlist").val()!=""){
        		alert("Here");
        		//$("#vidlist").attr('disabled', false).trigger("chosen:updated")
        		//this._references.$collectionVideoDropDownContainer = $('.js-collection-video-dropdown-container');
        		references.videodataFeed.addInputParam('limit', false, 0);
        		references.videodataFeed.setInputParam('limit', 0, true);
        		references.videodataFeed.addInputParam('state', false, $("#statelist").val());
        		references.videodataFeed.setInputParam('state', $("#statelist").val(), true);
				references.videodataFeed.addInputParam('partner', false, $("#partnerlist").val());
				references.videodataFeed.setInputParam('partner', $("#partnerlist").val(), true);
				references.videodataFeed.addInputParam('language', false, $("#langlist").val());
				references.videodataFeed.setInputParam('language', $("#langlist").val(), true);
				this.getCollectionVideoDropDown();
        	}
        	else{
        		//$("#vidlist").attr('disabled', true).trigger("chosen:updated");
        	}
        },
        
        _onVideoChosen: function(){
        	var vid = $("#vidlist").val();
        	var vidarray = this._references.videoarray;
        	var image;
        	for (var i=0; i<vidarray.length; i++)
        	{
        		if (vidarray[i].uid == vid){
        			image = vidarray[i].thumbnailURL16by9;
        		}
        	
        	}
        	
        	var renderData = {
                    title: $("#vidlist option:selected").text(),
        			uid:vid,
        			thumbnailURL:image,
                };
        	viewRenderer.renderAppend($('.js-carousel-container'), carouselTemplate, renderData);
        	$('#vidlist option[value=' + vid + ']').remove();
        	$("#vidlist").trigger("chosen:updated");
        	
        	$('#sortable li .video-remove').click(function(){
        		$('#vidlist').append(new Option($(this).parent().attr('data-title'), $(this).parent().attr('id')));
        		//var options =  $('#vidlist').attr('options');
        		//options[options.length] = newOption($(this).parent().attr('data-title'), $(this).parent().attr('id'));
        		$("#vidlist").trigger("chosen:updated");
        		$(this).parent().remove();
                
            });
        	
        },


        setInputParam: function(key, value, disableCacheClearing) {
            this._references.dataFeed.setInputParam(key, value, disableCacheClearing);
        },

        _onInputParamChanged: function() {
            this.getCollectionDropDown();
        },
        /**
         * Controller destructor
         * @return {void}
         */
        destroy: function() {
            this.base();

            // TODO: clean up
        }
    });

    return CollectionDropDownController;
});
