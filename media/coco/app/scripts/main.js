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
    'form_field_validator': 'libs/jquery.validate'
  }
});
 
require(['app'], function(app) {
  // use app here
  console.log(app);
  app.initialize();
});