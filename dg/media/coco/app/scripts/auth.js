define([
    'models/user_model',  
    'auth_offline_backend',
    'configs',
    'offline_utils',
    'jquery_cookie'
  ], function(User, OfflineAuthBackend, all_configs, Offline){
      
  var internet_connected = function(){
      return navigator.onLine;
  }
        
  var check_login = function(){
      var dfd = new $.Deferred()
      console.log("checking login");
      if(check_online_login())
      {
          check_offline_login()
              .done(function(){
                  dfd.resolve();
              })
              .fail(function(error){
                  dfd.reject(error);
              });
      }
      else
      {
          dfd.reject("Not logged in on server");
      }
      return dfd.promise();
  }

  //ideally shd have been exacty same as the server uses. But approximating it to avoid network request.
  var check_online_login = function(){
      if(!internet_connected||$.cookie('sessionid'))
          return true;
      return false;
  }
  
  //is exactly same as the offline backend uses. (Since offline backend auth is custom written by us)
  var check_offline_login = function(){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              if(User.get("loggedin"))
                  return dfd.resolve();
              else
                  return dfd.reject("User is currently logged out. (Offline Backend)");
          },
          error: function(){
               return dfd.reject("User couldn't be fetched from offline db");
          }
      });
      return dfd;
  }
  
  var logout = function(){
      var dfd = new $.Deferred();
      var that = this;
      online_logout()
          .always(function(){
              offline_logout()
                  .always(function(){
                      dfd.resolve();
                  })
          });
      return dfd;      
      // this.save_login_state_in_offline(User.get("username"), User.get("password"), false);
  }
  
  var online_logout = function(){
      var dfd = new $.Deferred();

      if(!internet_connected())
          dfd.resolve();
          
      $.post("/coco/logout/")
          .done(function(resp){
              return dfd.resolve();
          })
          .fail(function(resp){
              return dfd.reject(resp);
          });

      return dfd.promise();      
  }
  
  var offline_logout = function(){
      var dfd = new $.Deferred();
      OfflineAuthBackend.logout()
          .done(function(){
              dfd.resolve();
          })
          .fail(function(){
              dfd.reject();
          });
      return dfd;
  }
  
  var login = function(username, password){
      var dfd = new $.Deferred();
      console.log("Attemting login");
      if(internet_connected())
      {
          online_login(username, password)
              .fail(function(error){
                  console.log("Online login failed - "+error);
                  dfd.reject(error);
              })
              .done(function(){
                  offline_login(username, password)
                      .fail(function(error){
                          console.log("Offline login failed - "+error);
                          if(error == "No user found")
                          {     
                              offline_register(username, password)
                                  .fail(function(error){
                                      console.log("Offline register failed - "+error);
                                      dfd.reject(error);
                                  })
                                  .done(function(){
                                      console.log("Registered in Offline backend");
                                      console.log("Login Successfull");
                                      dfd.resolve();
                                  });      
                          }
                          else
                              dfd.reject(error);
                      })
                      .done(function(){
                          console.log("Login Successfull");
                          if(all_configs.misc.onLogin)
                              all_configs.misc.onLogin(Offline, this);
                          dfd.resolve();
                      });      
              });
      }
      else
      {
          offline_login(username, password)
              .fail(function(error){
                  console.log("Offline login failed - "+error);
                  if(error == "No user found")
                      dfd.reject("You need to be online till database has been downloaded.");
                  else
                      dfd.reject(error);
              })
              .done(function(){
                  console.log("Login Successfull");
                  if(all_configs.misc.onLogin)
                      all_configs.misc.onLogin(Offline, this);
                  dfd.resolve();
              });      
      }
      return dfd;
  }
  
  // resolves if server returns 1 or internet is not connected otherwise rejects
  var online_login = function(username, password){
      var dfd = new $.Deferred();
      if(!internet_connected())
          return dfd.resolve();
      $.post("/coco/login/", { "username": username, "password": password } )
          .done(function(resp){
              if(resp=="1")
                  return dfd.resolve();
              else 
                  return dfd.reject("Username or password is incorrect (Server)");
          })
          .fail(function(resp){
              return dfd.reject("Could not contact server. Try again in a minute.");
          });
      return dfd.promise();      
  }
  
  //resolves if u, p matches the one stored in off db 
  var offline_login = function(username, password){
      var dfd = new $.Deferred();
      OfflineAuthBackend.login(username, password)
          .done(function(){
              dfd.resolve();
          })
          .fail(function(error){
              dfd.reject(error);
          });
      return dfd.promise();
  }
  
  var offline_register = function(username, password){
      var dfd = new $.Deferred();
      OfflineAuthBackend.register(username, password)
          .done(function(){
              dfd.resolve();
          })
          .fail(function(error){
              dfd.reject(error);
          });
      return dfd.promise();
  }

  return {
    check_login: check_login,
    logout: logout,
    login: login
  };
});
