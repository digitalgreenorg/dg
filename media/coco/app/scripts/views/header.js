define([
  'jquery',
  'underscore',
  'backbone',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($){
    var HeaderView = Backbone.View.extend({
        // How many things to upload, button to go to the upload page
        // How many things to download, button to download
        // Name of the Current Page/View or maybe a breadcrumb

        events: {

        },
        template: _.template($('#header')
                    .html()),
        
        render: function(breadcrumb) {
            $(this.el)
                .html(this.template({
                breadcrumb: breadcrumb
            }));
            return this;
        },
        
        initialize: function(){
            // console.log(_);
            console.log("initializing header");
            return;
        }
    });
    
  // Our module now returns our view
  return HeaderView;
});