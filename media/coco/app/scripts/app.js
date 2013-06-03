define([
  'router', // Request router.js,
  'user_initialize'      
  ], function(Router, UserInitialize){
  var initialize = function(){
    // Pass in our Router module and call it's initialize function
    UserInitialize.run();
    Router.initialize();
  }

  return {
    initialize: initialize
  };
});
