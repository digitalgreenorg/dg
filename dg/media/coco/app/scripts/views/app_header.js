//This view the page header containt the branding, and the user profile - along with the username and logout action.
define(['jquery', 'underscore', 'configs', 'layoutmanager', 'models/user_model', 'auth'],

function(jquery, pass, configs, layoutmanager, User, Auth) {

    var HeaderView = Backbone.Layout.extend({
        template: "#page_header",
        events: {
            "click #logout": "logout",
            "click .js_language": "language",
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
            var language = User.get("language");
            return {
                username: username,
                language: language,
                configs: configs
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
            
            //keep the online-offline indicator up-to-date
            window.addEventListener("offline", this.user_offline);
            //keep the online-offline indicator up-to-date
            window.addEventListener("online", this.user_online);

            //set the online-offline indicator
            if (User.isOnline()) {
                this.user_online();
            } else {
                this.user_offline();
            }
        },
        
        //enable sync button, show online indicator
        user_online: function() {
            $('#sync')
                .removeAttr("disabled");
            $('#offline')
                .hide();
            $('#online')
                .show();
        },

        //disable sync button, show offline indicator
        user_offline: function() {
            $('#sync')
                .attr('disabled', true);
            $('#online')
                .hide();
            $('#offline')
                .show();
        },
        
        // logout and navigate to login url
        logout: function() {
            Auth.logout()
                .always(function() {
                window.location.href = window.location.origin + window.location.pathname;
            });
        },

        //this function is called when user clicks on language change options
        language: function(e) {
            e.preventDefault();
            var language_chosen = $(e.currentTarget).text();
            var language_current = User.get("language");
            if(language_chosen!=language_current){
                User.save({"language":language_chosen});
            }
        }
    });
    // Our module now returns our view
    return HeaderView;
});
