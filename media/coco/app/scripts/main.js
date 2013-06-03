require.config({
            
  
  paths: {
    'hm': 'libs/hm',
    'jquery': 'libs/jquery.min',
    'underscore': 'libs/backbone/underscore-min',
    'backbone': 'libs/backbone/backbone-min',
    'indexeddb-backbone': 'libs/indexeddb-backbonejs-adapter/backbone-indexeddb',
    'datatable': 'libs/datatablejs_media/js/jquery.dataTables.min',
    'form_field_validator': 'libs/jquery.validate',
    'layoutmanager': 'libs/layoutmanager/backbone.layoutmanager',
    'syphon':'libs/backbone.syphon',
    'bootstrapjs': 'libs/bootstrap/js/bootstrap.min',
    'chosen': 'libs/chosen/chosen.jquery.min',
    'date_picker': 'libs/bootstrap/js/bootstrap-datepicker',    
    'time_picker': 'libs/bootstrap/js/bootstrap-timepicker.min',    
  },
  
  shim:{
      'backbone': {
                      //These script dependencies should be loaded before loading
                      //backbone.js
                      deps: ['underscore', 'jquery'], // here I would like to load the already loaded library
                      exports: 'Backbone' 
                          }   , 
      'indexeddb-backbone': {
                      //These script dependencies should be loaded before loading
                      //backbone.js
                      deps: ['backbone'], // here I would like to load the already loaded library
                          }    ,
      'layoutmanager': {
                      //These script dependencies should be loaded before loading
                      //backbone.js
                      deps: ['backbone'], // here I would like to load the already loaded library
                          },
    'bootstrapjs': {
                  //These script dependencies should be loaded before loading
                  //backbone.js
                  deps: ['jquery'], // here I would like to load the already loaded library
                      },    
      'underscore': {
                    //These script dependencies should be loaded before loading
                    //backbone.js
                    deps: ['jquery'], // here I would like to load the already loaded library
                    exports: "_"
                        },    
    'datatable': {
                    deps:["jquery"]
                },
                                          
     'form_field_validator': {
                 deps:["jquery"]
     }  ,
     
     'syphon': {
                 deps:["jquery", "backbone"]
     },
     
     'bootstrapjs': {
                 deps:["jquery"]
     },
     'chosen': {
                 deps:["jquery"]
     },                                            
     'date_picker': {
                 deps:["jquery"]
     },                                            
     'time_picker': {
                 deps:["jquery"]
     },                                            

                  
  }
});
 
require(['app'], function(app) {
  // use app here
  console.log(app);
  app.initialize();
});