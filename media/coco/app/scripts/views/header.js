define([
  'jquery',
  'underscore',
  'backbone',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($){
    
    var HeaderView = Backbone.Layout.extend({
      template: "#header"
    });
    
  // Our module now returns our view
  return HeaderView;
});