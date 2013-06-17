define([
  'jquery',
  'backbone',
  // Using the Require.js text! plugin, we are loaded raw text
  // which will be used as our views primary template
  // 'text!templates/project/list.html'
], function($){
    
    var NotificationsView = Backbone.View.extend({
        el: '#notifications',
		error_notif_template: _.template($('#' + 'error_notifcation_template').html()),
        success_notif_template: _.template($('#' + 'success_notifcation_template').html()),
		
			
		add_alert : function(options){
			var notif_type = options.notif_type;
			var message = options.message;
			var alert_class, timeout, template;
			
			if (notif_type === "success"){
				template = this.success_notif_template({msg: message});
				alert_class = ".alert-success";
				timeout = 4000;
				
			}
			else
			{
				template = this.error_notif_template({msg: message});
				alert_class = ".alert-error";
				timeout = 7000;
				
			}
			$(this.el).append(template);
			$("html, body").animate({scrollTop: 0}, 700);
			
			window.setTimeout(function() {
				$(alert_class).fadeTo(500, 0)
				.slideUp(500, function(){
					$(this).remove(); 
				});
			}, timeout);	
		
		}
    });
    
  // Our module now returns our view
  return new NotificationsView;
});

