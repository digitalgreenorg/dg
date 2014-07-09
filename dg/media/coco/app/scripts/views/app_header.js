//This view the page header containt the branding, and the user profile - along with the username and logout action.
define(['jquery', 'underscore', 'configs', 'layoutmanager', 'models/user_model', 'auth'],

function(jquery, pass, configs, layoutmanager, User, Auth) {

    var HeaderView = Backbone.Layout.extend({
        template: "#page_header",
        events: {
            "click #logout": "logout"
        },
        
        initialize: function() {
            _(this)
                .bindAll('render');
            // Re-render the view when User model changes - to keep username updated    
            User.on('change', this.render);
        },

        serialize: function() {
            // Send username 
            var username = User.get("username");
            return {
                username: username,
            }
        },

        afterRender: function() { 
            console.log("rendering page_header");
            $( ".img-user" ).click(function(event) {
                // Stops the event from traveling up the hierarchy div-> container-> html.
                event.stopPropagation();
                $( ".user-dropdown" ).toggle();
            });
            
            // Hide dropdown if clicked anywhere outside the dropdown.
            $( "html" ).click(function() {
                $( ".user-dropdown" ).hide();
            });
        },
        // logout and navigate to login url
        logout: function() {
            Auth.logout()
                .always(function() {
                window.location.href = window.location.origin + window.location.pathname;
            });
        }
    });


    // Our module now returns our view
    return HeaderView;
});
