define([
  'jquery',
  'underscore',
  'backbone',
  'indexeddb-backbone',
  'router' // Request router.js,
  ], function($, _, Backbone, pass,Router){
  var initialize = function(){
    // Pass in our Router module and call it's initialize function
    Router.initialize();
  }

  return {
    initialize: initialize
  };
});
