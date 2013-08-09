define([
    'models/user_model',  
  ], function(User){
      
  //sets login state = false in off db
  var logout = function(){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              save_login_state_in_offline(User.get("username"), User.get("password"), false)
                  .done(function(){
                      dfd.resolve();
                  })
                  .fail(function(){
                      dfd.reject();
                  });
          },
          error: function(){
               return dfd.reject();
          }
      });      
      return dfd;
  }
  
  // if u, p matches that in off db sets login state = true else false
  var login = function(username, password){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              if(username==User.get("username") && password==User.get("password"))
              {
                  save_login_state_in_offline(username, password, true)
                      .done(function(){
                          return dfd.resolve("Successfully Logged In (Offline Backend)");
                      })
                      .fail(function(error){
                          return dfd.reject(error);
                      });
              }
              else
              {
                  return dfd.reject("Username password did not match (Offline Backend)");
              }
          },
          error: function(){
               return dfd.reject("No user found");
          }
      });
      return dfd.promise();
  }
  
  var register = function(username, password){
      var dfd = new $.Deferred();
      User.save({
          key: "user_info",
          username: username,
          password: password,
          loggedin: true
      },{
          success: function(){
              dfd.resolve();
          },
          error: function(){
              dfd.reject();
          }
      });
      return dfd;
  }
  
  //saves in offline that this username, password is logged in/out
  var save_login_state_in_offline = function(username, password, loggedin){
      var dfd = new $.Deferred();
      User.save({'username':username, 'password':password, 'loggedin':loggedin},{
          success: function(){
              console.log("user state saved in offline");
              dfd.resolve();
          },
          error: function(){
              console.log("Error while saving login state in offline (Offline Backend)");
              dfd.reject("Error while saving login state in offline (Offline Backend)");
          }
      });
      return dfd;
  }
  
  
  var check_login = function(){
      var dfd = new $.Deferred();
      User.fetch({
          success: function(){
              if(User.get("loggedin"))
                  return dfd.resolve();
              else
                  return dfd.reject("User is currently logged out. (Offline Backend)");
          },
          error: function(){
               return dfd.reject("User couldn't be fetched from offline db (Offline Backend)");
          }
      });
      return dfd;
  }
  
  var check_login_approx = function(){
      return User.get("loggedin");
  }

  return {
    login: login,
    logout: logout,
    register: register,
    check_login: check_login,
    check_login_approx: check_login_approx
  };
});
