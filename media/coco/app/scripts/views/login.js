define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'models/user_model',
    'auth',
	'offline_utils'
], function(jquery, underscore, backbone, layoutmanager, User, Auth, Offline){
    
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
          User.fetch({
              success: function(model){
                  console.log("USERMODEL : successfully fetched");
                  that.render();
              },
              error: function(){
                  console.log("USERMODEL :  fetch failed") 
                  that.render();           
              }
          });
          
      },
      
      serialize: function(){
          return User.toJSON();
      },
      
      scrap_view: function(){
           this.$('#login_modal').modal('hide');  
           this.remove();   
      },
      
      afterRender: function(){
          console.log("rendered login view");
          this.$('#login_modal').modal({
              keyboard: false,
              backdrop: "static",
          });
          this.$('#login_modal').modal('show');
      },
      
      //fetches u,p from dom  and asks auth module to login
      attempt_login: function(e){
		  e.preventDefault();
          console.log("login attempted");
          this.set_login_button_state('loading');
          var username = this.$('#username').val();
          var password = this.$('#password').val();
          var that = this;
          Auth.login(username, password)
              .done(function(){
                  that.scrap_view();
                  window.Router.navigate("", {
                      trigger:true
                  });
              })
              .fail(function(error){
			      $("#password").val('');
				  that.$('#error_msg').html(error);
                  that.set_login_button_state('reset');
              });
      },
      
      set_login_button_state: function(state){
          if(state=="disabled")
              this.$("#login_button").attr("disabled",true);    
          else
              this.$("#login_button").button(state);    
      },
	  
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