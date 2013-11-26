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
    var CollectionAddDataFeed = require('app/libs/CollectionsAddDataFeed');
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
            this._dropdownChosen();
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();
            var references = this._references;
            references.dataFeed = new CollectionDropDownDataFeed();
            references.videodataFeed = new CollectionVideoDropDownDataFeed();
            references.addDataFeed = new CollectionAddDataFeed();
            references.$collectionAddWrapper = $referenceBase;
            references.$collectionDropDownContainer = $referenceBase.find('.js-collection-dropdown-container');
            references.$saveButton = $referenceBase.find('.collection-save-button');
            references.$collectionTitle = $referenceBase.find('.coltitle');
        },

        _initEvents: function() {
            this.base();
            var boundFunctions = this._boundFunctions;
            var references = this._references;
            
            //boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            //references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);
            
            boundFunctions.onVideoDataProcessed = this._onVideoDataProcessed.bind(this);
            references.videodataFeed.on('dataProcessed', boundFunctions.onVideoDataProcessed);
            
            boundFunctions.onSaveCollectionClick = this._onSaveCollectionClick.bind(this);
            references.$saveButton.on("click", boundFunctions.onSaveCollectionClick);
            
            this._boundFunctions.onDropDownChosen = this._onDropDownChosen.bind(this);
            $(".js-dropdown").on('change', this._boundFunctions.onDropDownChosen);
            
            this.checkforedit();
            
        },
        
        checkforedit: function(){
            if ($('.js-uid').data('collectionuid')){
                $("#partnerlist").val($('.va-dropdown').data('collectionpartner')).change();
                $("#statelist").val($('.va-dropdown').data('collectionstate')).change();
                $("#langlist").val($('.va-dropdown').data('collectionlanguage')).change();
            }
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
            
            if ($('.js-uid').data('collectionuid')){
            var videos_collection = $('.js-collection-video-dropdown-container').data('videos');
            var a;
            for (a in videos_collection){
                console.log(videos_collection[a]);
                $("#vidlist").val(videos_collection[a]).change();
            }
            
            $("#vidlist").trigger("chosen:updated");
            }
            
        },
        _onDataProcessed: function() {
            this.getCollectionDropDown();
        },
        
        _onVideoDataProcessed: function() {
        	this.getCollectionVideoDropDown();
        },

        afterCollectionAdd: function(){
            var url = "/discover" +"/"+ $("#partnerlist :selected").text() +"/"+ $("#statelist").val() +"/"+ $("#langlist").val() +"/"+ $('.coltitle').val()
            window.location.assign(url)
        },
        
        _onSaveCollectionClick: function(e) {
        	e.preventDefault();
        	var order = $( "#sortable" ).sortable('toArray');
        	var references = this._references;
        	if ($('.js-uid').data('collectionuid')){
        	    references.addDataFeed.addInputParam('uid', false, $('.js-uid').data('collectionuid'));
        	    references.addDataFeed.setInputParam('uid', $('.js-uid').data('collectionuid'), true);
        	}
        	references.addDataFeed.addInputParam('title', false, references.$collectionTitle.val());
            references.addDataFeed.addInputParam('partner', false, $("#partnerlist").val());
            references.addDataFeed.addInputParam('language', false, $("#langlist").val());
            references.addDataFeed.addInputParam('state', false, $("#statelist").val());
            references.addDataFeed.addInputParam('videos', false, order);
            
            references.addDataFeed.setInputParam('title', references.$collectionTitle.val(), true);
            references.addDataFeed.setInputParam('partner', $("#partnerlist").val(), true);
            references.addDataFeed.setInputParam('language', $("#langlist").val(), true);
            references.addDataFeed.setInputParam('state', $("#statelist").val(), true);
            references.addDataFeed.setInputParam('videos', order, true);
            
            
            references.addDataFeed._fetch(null, this.afterCollectionAdd.bind(this), 'POST');
        	
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
        		references.videodataFeed.addInputParam('limit', false, 0);
        		references.videodataFeed.setInputParam('limit', 0, false);
        		references.videodataFeed.addInputParam('state', false, $("#statelist").val());
        		references.videodataFeed.setInputParam('state', $("#statelist").val(), false);
				references.videodataFeed.addInputParam('partner', false, $("#partnerlist").val());
				references.videodataFeed.setInputParam('partner', $("#partnerlist").val(), false);
				references.videodataFeed.addInputParam('language', false, $("#langlist").val());
				references.videodataFeed.setInputParam('language', $("#langlist").val(), false);
				this.getCollectionVideoDropDown();
        	}
        	else{
        	//TODO: What happens if value becomes default again
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
        		$('#vidlist').append(new Option($(this).parent().attr('data-title'), $(this).parent().attr('id').trim()));
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
