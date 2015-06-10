define([
    'jquery',
    'underscore',
    'backbone',
    'layoutmanager',
    'models/user_model',
    'auth',
    'offline_utils',
], function(jquery, underscore, backbone, layoutmanager, User, Auth, Offline){
    
    var FileView = Backbone.Layout.extend({
      template: "#file_upload",
      events:{
          'click #upload_button': 'read_file',
      },
      
      initialize: function(){
          console.log("Initializing login view");
          _(this).bindAll('render');
          var that = this;
          that.render();
      },
      
      serialize: function(){
          // send the user info to the template
          return User.toJSON();
      },
      
      scrap_view: function(){
           this.$('#file_modal').modal('hide');
           $('.modal-backdrop').remove();
      },
      
      afterRender: function(){
          this.$('#file_modal').modal({
              keyboard: false,
              backdrop: "static",
         });
      },
      
      //fetches u,p from dom  and asks auth module to login
      read_file: function(e){
          e.preventDefault();
          console.log("login attempted");
          var that = this
          var fileInput = document.getElementById('fileupload');
          var file = fileInput.files[0];
          var reader = new FileReader();

          reader.onload = function(e) {
              var obj = JSON.parse(reader.result);
              alert(obj);
              that.scrap_view();
              //var off_coll = Offline.create_b_collection('video');
              //off_coll.reset()
              Offline.delete_object(null, 'video', 1548);
              //_.invoke(off_coll.toArray(), 'destroy');
          }

          reader.readAsText(file);
          
      }
    });
    
  // Our module now returns our view
  return FileView;
});