$(function(){
  
  // country model
  var Country = Backbone.Model.extend({
                                      remove: function() {
                                      this.destroy();
                                      },
                                      url : function() {
                                      return this.id ? '/api/v1/block/' + this.id+"/" : '/api/v1/block/';
                                      } 
  
  });
  
  // set up the view for a country
  var CountryView = Backbone.View.extend({
                                            tagName:'tr',
                                            events: {
                                                 "click a.edit" : "editCountry",
                                                 "click a.destroy" : "remove"
                                            },
                                             
                                            editCountry: function(event) {
                                                 event.preventDefault();
                                                 event.stopImmediatePropagation();
                                                 // call back up to the main app passing the current model for it
                                                 // to allow a user to update the details
                                                 this.options.app.editCountry(this.model);
                                            },
                                             
                                            remove: function(event) {
                                                 event.stopImmediatePropagation();
                                                 event.preventDefault();
                                                 if (confirm("Are you sure you want to delete this entry?"))
                                                 {
                                                    this.model.remove();
                                                 }
                                            },

                                            template:_.template($('#tpl-block-item').html()),
                                             render: function () {
                                                $(this.el).html(this.template(this.model.toJSON()));
                                                return this;
                                            }
                                          });
  
  // define the collection of countries
  var CountryCollection = Backbone.Collection.extend({
                                                        model: Country,
                                                        url: '/api/v1/block/',
                                                        parse: function(data) {
                                                        return data.objects;
                                                     }
                                                     
                                                      });
  
  // main app
  var AppView = Backbone.View.extend({
                                     el: $("body"),
                                     events: {
                                        "click button#add" : "addCountry",
                                         "click #blockForm :submit": "handleModal",
                                         "keydown #blockForm": "handleModalOnEnter",
                                         "hidden #blockModal": "prepareForm"
                                     },
                                     
                                     initialize: function() {
                                         // instantiate a country collection
                                         this.countries = new CountryCollection();
                                         this.countries.bind('all', this.render, this);
                                         this.countries.fetch();
                                     },
                                     
                                     render: function () {
                                        $('#t').html('');
                                         this.countries.each(function (country) {
                                                                $('#t').append(new CountryView({model: country,app:this}).render().el);
                                                             }, this);
                                         
                                         return this;
                                     },
                                    
                                     addCountry: function(event){
                                         event.stopImmediatePropagation();
                                         event.preventDefault();
                                         this.prepareForm(null);
                                         $('#blockModal').modal('show');
   
                                     },
                                     
                                     addNew: function(country){
                                     alert(JSON.stringify(country));
                                        this.countries.create(country,{wait: true});
                                     

                                     },
                                     
                                     editCountry: function(country){
                                         this.prepareForm(country.toJSON());
                                         $('#blockModal').data('countryId', country.get('id'));
                                         $('#blockModal').modal('show');
                                     },
                                     
                                     prepareForm: function(countryData) {
                                         countryData = countryData || {};
                                         var data = {
                                         'block_name': '',
                                         'start_date': '',
                                         
                                         };
                                         
                                         $.extend(data, countryData);
                                         
                                         var form = $('#blockForm');
                                         $(form).find('#id_block_name').val(data.block_name);
                                         $(form).find('#id_start_date').val(data.start_date);
                                         // clear any previous references to countryId in case the user
                                         // clicked the cancel button
                                         $('#blockModal').data('countryId', '');
                                     },
                                     
                                     handleModal: function(event) {
                                         event.preventDefault();
                                         event.stopImmediatePropagation();
                                         var form = $('#blockForm');
                                         
                                         var countryData = {
                                             block_name: $(form).find('#id_block_name').val(),
                                             start_date: $(form).find('#id_start_date').val(),
                                             district: "/api/v1/district/"+$(form).find('#id_district').val()+"/",
                                         };
                                         
                                         if ($('#blockModal').data('countryId'))
                                         {
                                             countryData.id = $('#blockModal').data('countryId');
                                             this.updateCountry(countryData);
                                         }
                                         else
                                         {
                                             // add or update the country
                                             this.addNew(countryData);
                                         }
                                         
                                         // hide the modal
                                         $('#blockModal').modal('hide');
                                         
                                         return this;
                                     },
                                     
                                     handleModalOnEnter: function(event) {
                                        // process the modal if the user pressed the ENTER key
                                         if (event.keyCode == 13)
                                         {
                                         return this.handleModal(event);
                                         }
                                     },
                                     
                                     updateCountry: function(countryData){
                                        var country = this.countries.get(countryData.id)
                                         if (_.isObject(country))
                                         {
                                             // iterate through all the data in countryData, setting it
                                             // to the country model
                                             for (var key in countryData)
                                             {
                                                 // ignore the ID attribute
                                                 if (key != 'id')
                                                 {
                                                    country.set(key, countryData[key]);
                                                 }
                                             }
                                             
                                             // persist the change
                                             country.save({wait: true});
                                         }
                                     
                                     
                                     }

                                 });
  
  var app = new AppView;
  });


