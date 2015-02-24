// The view for login. Its responsibiltiy is to show the login form to user and uses auth.js module to do the actual authentication.
define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'models/user_model',
    'auth',
	'offline_utils', 
	'configs',
], function(jquery, underscore, backbone, layoutmanager, User, Auth, Offline, all_configs){
    
    var LoginView = Backbone.Layout.extend({
      template: "#login",
      events:{
          'click #login_button': 'attempt_login',
		  'click #change_user' : 'change_user'		  
      },
      
      initialize: function(){
          console.log("Initializing login view");
          _(this).bindAll('render');
          var that = this;
          that.render();
      },
      
      serialize: function(){
          var s_passed = {};
          
          // name of the entity bieng added/edited
          
          // send the user info to the template
          s_passed["user"] = User.toJSON();
          s_passed["configs"] = all_configs;
          return s_passed;
      },
      
      scrap_view: function(){
           this.$('#login_modal').modal('hide');
           $('.modal-backdrop').remove();
      },
      
      afterRender: function(){
          console.log("rendered login view");
          //render the modal
          User.fetch({
              success: function(model){
                  console.log("USERMODEL : successfully fetched");
                  this.$('#login_modal').modal({
                       keyboard: false,
                       backdrop: "static",
                  });
              },
              error: function(){
                  console.log("USERMODEL :  fetch failed") 
                  this.$('#login_modal').modal({
                      keyboard: false,
                      backdrop: "static",
                  });           
              }
          });
      },
      
      //fetches u,p from dom  and asks auth module to login
      attempt_login: function(e){
		  e.preventDefault();
          console.log("login attempted");
          this.set_login_button_state('loading');
          var username = this.$('#username').val();
          var password = this.$('#password').val();
          var language = this.$('#language').val();
          var that = this;
          // use the auth module to authenticate
          if (language != ''){
              Auth.login(username, password, language)
                  .done(function(){
                      //login successfull - route to the home view
                      that.scrap_view();
                      window.Router.navigate("", {
                          trigger:true
                      });
                  })
                  .fail(function(error){
                      // authentication failed
                      // clear the password
    			      $("#password").val('');
                      // show the error
    				  that.$('#error_msg').html(error);
                      that.set_login_button_state('reset');
                  });
          }
          else{
              that.$('#error_msg').html("Language not Selected");
              that.set_login_button_state('reset');
          }
      },
      
      // set state of login button - disable while authentication request is under process
      set_login_button_state: function(state){
          if(state=="disabled")
              this.$("#login_button").attr("disabled",true);    
          else
              this.$("#login_button").button(state);    
      },
	  
      // to login with different user - clear the offline db of existing user
	  change_user: function(){
		var val = confirm("Your current database will be deleted and a new database will be downloaded");
		if (val==true){
			Offline.reset_database();
		}
	  }
      
    });
    
  // Our module now returns our view
  return LoginView;
});