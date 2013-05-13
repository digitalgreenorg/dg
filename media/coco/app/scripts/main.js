require.config({
  shim: {
  },
            
  
  paths: {
    'hm': 'libs/hm',
    'esprima': 'libs/esprima',
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
  
  shims:{
      'backbone': {
                      //These script dependencies should be loaded before loading
                      //backbone.js
                      deps: ['underscore', 'jquery'], // here I would like to load the already loaded library
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
                    export: "_"    
                        },    
                              
                                                    

                  
  }
});
 
require(['app'], function(app) {
  // use app here
  console.log(app);
  app.initialize();
});