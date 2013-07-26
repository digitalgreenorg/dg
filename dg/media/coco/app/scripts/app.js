define([
  'router', // Request router.js,
  'user_initialize',
  'views/app_layout',
  ], function(Router, UserInitialize, AppLayout){
  
  var framework_initialize = function(){
      $.ajaxSetup({
          crossDomain: false, // obviates need for sameOrigin test
          beforeSend: function(xhr, settings) {
              if (!csrfSafeMethod(settings.type)) {
                  xhr.setRequestHeader("X-CSRFToken", get_csrf());
              }
          },
      });
      
      $(document).ajaxError(function(event, jqxhr, settings, exception) {
          if(jqxhr.status==401)
              window.Router.navigate("login",{trigger:true});               
      });
      
      $("#app").empty().append(AppLayout.el);
      AppLayout.render();
  };
  
  var get_csrf = function(){
      return $.cookie('csrftoken');
  };
  
  function csrfSafeMethod(method) {
      // these HTTP methods do not require CSRF protection
      return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
  };
  
  var update_appcache = function(){
      $(window).load(function(){
          window.applicationCache.addEventListener('updateready', function(e) {
            if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
              // Browser downloaded a new app cache.
              // Swap it in and reload the page to get the new hotness.
              window.applicationCache.swapCache();
              if (confirm('A new version of this site is available. Load it?')) {
                window.location.reload();
              }
            } else {
              // Manifest didn't changed. Nothing new to server.
            }
          }, false);
      });
  };

  // runs the initiaize of framweork, user and then start router  
  //wait till dom is ready
  var initialize = function(){
      update_appcache();
      //wait till dom is ready
      $(function(){
          framework_initialize();
          UserInitialize.run();
          Router.initialize();
      });
  };

  return {
    initialize: initialize
  };
});
