define([
  'router', // Request router.js,
  'user_initialize'      
  ], function(Router, UserInitialize){
  
  var framework_initialize = function(){
      $.ajaxSetup({
          crossDomain: false, // obviates need for sameOrigin test
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type)) {
                  xhr.setRequestHeader("X-CSRFToken", get_csrf());
              }
          },
          error: function(xhr, status, error){
              if(xhr.status == 401)
              {
                  window.Router.navigate("login",{trigger:true});
              }
          }
      });      
  };
  
  var get_csrf = function(){
      return $.cookie('csrftoken');
  };
  
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };

  // runs the initiaize of framweork, user and then start router  
  var initialize = function(){
    framework_initialize();
    UserInitialize.run();
    Router.initialize();
  };

  return {
    initialize: initialize
  };
});
