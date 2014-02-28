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
    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var jQuery = require('jquery');
    var Select2 = require('libs/external/select2');
    
    var PracticeMappingDataFeed = require('app/libs/PracticeMappingDataFeed');
    var CollectionVideoDropDownDataFeed = require('app/libs/CollectionVideoDropDownDataFeed');
    var CollectionAddDataFeed = require('app/libs/CollectionsAddDataFeed');
    
    var practiceMappingTemplate = require('text!app/views/practice-mapping.html');
    var collectionVideoDropDownTemplate = require('text!app/views/collection-add-video-dropdown.html');
    var carouselTemplate = require('text!app/views/collection-add-video-carousel.html');
    
    var CollectionDropDownController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);
            this.getPracticeMapping();
            this._dropdownChosen();
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();
            var references = this._references;
            references.dataFeed = new PracticeMappingDataFeed();
            references.videodataFeed = new CollectionVideoDropDownDataFeed();
            references.addDataFeed = new CollectionAddDataFeed();
            references.$collectionAddWrapper = $referenceBase;
            references.$collectionUid = $referenceBase.find('.js-uid').data('collectionuid');
            references.$metaInformationContainer = $referenceBase.find('.js-meta-dropdown');
            references.$videoDropDownContainer = $referenceBase.find('.js-collection-video-dropdown-container');
            references.$practiceMappingContainer = $referenceBase.find('.js-collection-mapping-container');
            references.$saveButton = $referenceBase.find('.collection-save-button');
            references.$collectionTitle = $referenceBase.find('.coltitle');
            references.$dropDown = $referenceBase.find('.js-dropdown');
            references.$partnerList = $referenceBase.find('#partnerlist');
            references.$stateList = $referenceBase.find('#statelist');
            references.$langList = $referenceBase.find('#langlist');
        },

        _initEvents: function() {
            this.base();
            var boundFunctions = this._boundFunctions;
            var references = this._references;
            
            boundFunctions.onDataProcessed = this._onDataProcessed.bind(this);
            references.dataFeed.on('dataProcessed', boundFunctions.onDataProcessed);
            
            boundFunctions.onVideoDataProcessed = this._onVideoDataProcessed.bind(this);
            references.videodataFeed.on('dataProcessed', boundFunctions.onVideoDataProcessed);
            
            boundFunctions.onSaveCollectionClick = this._onSaveCollectionClick.bind(this);
            references.$saveButton.on("click", boundFunctions.onSaveCollectionClick);
            
            this._boundFunctions.onDropDownChosen = this._onDropDownChosen.bind(this);
            references.$dropDown.on('change', this._boundFunctions.onDropDownChosen);
            
            this.checkforedit();
            
        },
        
        checkforedit: function(key){
            var references = this._references;
            if (references.$collectionUid){
                if (key == 'mapping'){
                    references.$catList.val(references.$practiceMappingContainer.data('category').trim()).change();
                    references.$subCatList.val(references.$practiceMappingContainer.data('subcategory').trim()).change();
                    references.$topicList.val(references.$practiceMappingContainer.data('topic').trim()).change();
                    references.$subTopicList.val(references.$practiceMappingContainer.data('subtopic').trim());
                    references.$subjectList.val(references.$practiceMappingContainer.data('subject').trim());
                }
                else{
                    references.$partnerList.val(references.$metaInformationContainer.data('collectionpartner')).change();
                    references.$stateList.val(references.$metaInformationContainer.data('collectionstate')).change();
                    references.$langList.val(references.$metaInformationContainer.data('collectionlanguage')).change();
                }
                
            }
        },
        
        
        getPracticeMapping: function() {
            var practicemappingData = this._references.dataFeed.getPracticeMapping();
            if (practicemappingData == false) {
                return false;
            }
            this._references.mapping = practicemappingData;
            this._renderPracticeMapping(practicemappingData);
            
            this.checkforedit('mapping');
            this._dropdownChosen();
            
            
        },

        getCollectionVideoDropDown: function() {
            var references = this._references
            var collectionvideodropdownData = references.videodataFeed.getCollectionVideoDropDown();
            if (collectionvideodropdownData == false) {
                return false;
            }
            references.videoarray = collectionvideodropdownData;
            this._renderVideoCollectionDropDown(collectionvideodropdownData);
            
            if (references.$collectionUid){
            var videos_collection = references.$videoDropDownContainer.data('videos');
            var a;
            for (a in videos_collection){
                console.log(videos_collection[a]);
                references.$vidList.val(videos_collection[a]).change();
            }
            
            }
            
        },
        _onDataProcessed: function() {
            this.getPracticeMapping();
        },
        
        _onVideoDataProcessed: function() {
        	this.getCollectionVideoDropDown();
        },

        afterCollectionAdd: function(){
            alert('added')
            var url = "/discover" +"/"+ $("#partnerlist :selected").text() +"/"+ $("#statelist").val() +"/"+ $("#langlist").val() +"/"+ $('.coltitle').val()
            window.location.assign(url)
        },
        
        _onSaveCollectionClick: function(e) {
        	e.preventDefault();
        	var order = $( "#sortable" ).sortable('toArray');
        	var references = this._references;
        	if (references.$collectionUid){
        	    references.addDataFeed.addInputParam('uid', false, references.$collectionUid);
        	    references.addDataFeed.setInputParam('uid', references.$collectionUid, true);
        	}
        	references.addDataFeed.addInputParam('title', false, references.$collectionTitle.val());
            references.addDataFeed.addInputParam('partner', false, references.$partnerList.val());
            references.addDataFeed.addInputParam('language', false, references.$langList.val());
            references.addDataFeed.addInputParam('state', false, references.$stateList.val());
            references.addDataFeed.addInputParam('videos', false, order);
            references.addDataFeed.addInputParam('category', false, references.$catList.val());
            references.addDataFeed.addInputParam('subcategory', false, references.$subCatList.val());
            references.addDataFeed.addInputParam('topic', false, references.$topicList.val());
            references.addDataFeed.addInputParam('subtopic', false, references.$subTopicList.val());
            references.addDataFeed.addInputParam('subject', false, references.$subjectList.val());
            
            
            references.addDataFeed.setInputParam('title', references.$collectionTitle.val(), true);
            references.addDataFeed.setInputParam('partner', $("#partnerlist").val(), true);
            references.addDataFeed.setInputParam('language', $("#langlist").val(), true);
            references.addDataFeed.setInputParam('state', $("#statelist").val(), true);
            references.addDataFeed.setInputParam('videos', order, true);
            references.addDataFeed.setInputParam('category', $("#catlist").val(), true);
            references.addDataFeed.setInputParam('subcategory', $("#subcatlist").val(), true);
            references.addDataFeed.setInputParam('topic', $("#topiclist").val(), true);
            references.addDataFeed.setInputParam('subtopic', $("#subtopiclist").val(), true);
            references.addDataFeed.setInputParam('subject', $("#subjectlist").val(), true);
            
            if (references.$collectionUid){
                references.addDataFeed._fetch(null, this.afterCollectionAdd.bind(this), 'PUT');
            }
            else{
                references.addDataFeed._fetch(null, this.afterCollectionAdd.bind(this), 'POST');
            }
            
        	
        },
        _renderPracticeMapping: function(practicemappingData) {
            var references = this._references;
            var category = [];
            var arr;
            for (arr in practicemappingData){
                category.push(arr);
            }
            var renderData = {
                    category: category.sort()
                };
            var renderedPracticeMapping = viewRenderer.render(practiceMappingTemplate, renderData);
            this._references.$practiceMappingContainer.html(renderedPracticeMapping);
            this._references.category = category.sort();
            
            references.$catList = jQuery('#catlist');
            references.$subCatList = jQuery('#subcatlist');
            references.$topicList = jQuery('#topiclist');
            references.$subTopicList = jQuery('#subtopiclist');
            references.$subjectList = jQuery('#subjectlist');
            
            this._boundFunctions.onCategoryChosen = this._onCategoryChosen.bind(this);
            references.$catList.on('change', this._boundFunctions.onCategoryChosen);
            
            this._boundFunctions.onsubCategoryChosen = this._onsubCategoryChosen.bind(this);
            references.$subCatList.on('change', this._boundFunctions.onsubCategoryChosen);
            
            this._boundFunctions.onTopicChosen = this._onTopicChosen.bind(this);
            references.$topicList.on('change', this._boundFunctions.onTopicChosen);
            
            
        },
        
        _renderVideoCollectionDropDown: function(collectionvideodropdownData) {
            var references = this._references
            
            var renderData = {
                     video: collectionvideodropdownData
            };
            
            var renderedCollectionVideoDropDown = viewRenderer.render(collectionVideoDropDownTemplate, renderData);
            
            references.$videoDropDownContainer.html(renderedCollectionVideoDropDown);
            
            references.$vidList = jQuery('#vidlist')
            
            this._boundFunctions.onVideoChosen = this._onVideoChosen.bind(this);
            references.$vidList.on('change', this._boundFunctions.onVideoChosen);
            
            this._dropdownChosen();
        },

        _dropdownChosen: function(){
        	var references = this._references;
        	try{
        	    $(".chosen-select").select2({no_results_text: "No results match", width: "90%"});
        	   }
        	catch(err){
        	    $("select.chosen-select").select2({no_results_text: "No results match", width: "90%"});
        	}
            
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
        
        _onCategoryChosen: function(){
            var references = this._references
            var category_name = references.$catList.val();
            
            var mapping_data = this._references.mapping;
            
            references.$subCatList.find('option:not(:first)').remove();
            references.$topicList.find('option:not(:first)').remove();
            references.$subTopicList.find('option:not(:first)').remove();
            references.$subjectList.find('option:not(:first)').remove();
            
            var subcategory = mapping_data[category_name]
            var arr;
            for (arr in subcategory){
                if (arr != 'subject'){
                    references.$subCatList.append( new Option(arr,arr) );
                }
            }
            
            var subject = (mapping_data[category_name]['subject']).sort();
            var i;
            for (i in subject){
                references.$subjectList.append( new Option(subject[i],subject[i]) );
            }
            
            this._dropdownChosen();

        },
        
        _onsubCategoryChosen: function(){
            var references = this._references
            
            var category_name = references.$catList.val();
            var subcategory_name = references.$subCatList.val();
            var subject_name = references.$subjectList.val();
            var mapping_data = references.mapping;
            
            references.$topicList.find('option:not(:first)').remove();
            references.$subTopicList.find('option:not(:first)').remove();
            
            var topic=[];
            var arr;
            for (arr in mapping_data[category_name][subcategory_name]){
                topic.push(arr);
                references.$topicList.append( new Option(arr,arr) );
            }
            this._dropdownChosen();
        },
        
        _onTopicChosen: function(){
            var references = this._references
            
            var category_name = references.$catList.val();
            var subcategory_name = references.$subCatList.val();
            var subject_name = references.$subjectList.val();
            var topic_name = references.$topicList.val();
            var mapping_data = references.mapping;
            
            var subtopic=mapping_data[category_name][subcategory_name][topic_name];
            subtopic=subtopic.sort()
            
            references.$subTopicList.find('option:not(:first)').remove();
            
            var i;
            for (i in subtopic){
                references.$subTopicList.append( new Option(subtopic[i],subtopic[i]) );
            }
            this._dropdownChosen();
        },
        
        _onVideoChosen: function(){
            var references = this._references
            var vid = references.$vidList.val();
            var vidarray = this._references.videoarray;
            var image;
            var title;
            for (var i=0; i<vidarray.length; i++)
            {
                if (vidarray[i].uid == vid){
                    title = vidarray[i].title;
                    image = vidarray[i].thumbnailURL16by9;
                }
            }
        	
            var renderData = {
                    title: title,
                    uid:vid,
                    thumbnailURL:image,
                };
        	viewRenderer.renderAppend($('.js-carousel-container'), carouselTemplate, renderData);
        	references.$vidList.find('option[value=' + vid + ']').remove();
        	references.$vidList.select2("val", "");
        	
        	$('#sortable li .video-remove').click(function(){
        		$('#vidlist').append(new Option($(this).parent().attr('data-title'), $(this).parent().attr('id').trim()));
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
