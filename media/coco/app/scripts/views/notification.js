define([
  'jquery',
  'underscore',
  'backbone',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($){
    
    var NotificationsView = Backbone.View.extend({
        el: '#notifications'
    });
    
  // Our module now returns our view
  return new NotificationsView;
});