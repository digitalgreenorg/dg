define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'models/user_model',
    'auth'  
], function(jquery, underscore, backbone, layoutmanager, User, Auth){
    
    var LoginView = Backbone.Layout.extend({
      template: "#login",
      events:{
          'click #login_button': 'attempt_login'                  
      },
      
      initialize: function(router){
          console.log("Initializing login view");
          this.router = router;
          _(this).bindAll('render');
          var that = this;
          this.$('#login_modal').modal({
              keyboard: false,
              backdrop: "static",
          });
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
          this.$('#login_modal').modal('show');
      },
      
      //fetches u,p from dom  and asks auth module to login
      attempt_login: function(e){
		  e.preventDefault();
          console.log("login attempted");
          var username = this.$('#username').val();
          var password = this.$('#password').val();
          var that = this;
          Auth.login(username, password)
              .done(function(){
                  that.scrap_view();
                  that.router.navigate("", {trigger:true});
              })
              .fail(function(error){
                  that.$('#error_msg').html(error);
              });
      },
      
    });
    
  // Our module now returns our view
  return LoginView;
});