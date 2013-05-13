define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb-backbone',
  'router', // Request router.js,
  'bootstrapjs',
  'user_initialize'      
  ], function($, _, Backbone, pass,Router, pass,UserInitialize){
  var initialize = function(){
    // Pass in our Router module and call it's initialize function
    UserInitialize.run();
    Router.initialize();
  }

  return {
    initialize: initialize
  };
});
