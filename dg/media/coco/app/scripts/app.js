//  Initializes application. 
// - updates appcache
// - runs framework intitialize:
//     * configures all ajax POST /PUT requests to set csrf token
//     * configures ajax requests to navigate to login url in case 401 error is recvd
//     * puts in the parent view of application - app_layout
// - runs initialization specified by user in user_initialize.js
// - starts router - Router takes over from here.

define(['router', 'user_initialize', 'views/app_layout', ], function(Router, UserInitialize, AppLayout) {

    var initialize = function() {
        //check for appcache update
        update_appcache(); 
        //wait till dom is ready
        $(function() {
            //initialize framework
            framework_initialize();
            //run any initialization logic defined by framework user in user_initialize.js 
            UserInitialize.run();
            //start the router - the router takes over from here 
            Router.initialize(); 
        });
    };


    var framework_initialize = function() {
        //globally configure ajax requests to set csrf token header for authentication
        $.ajaxSetup({
            // obviates need for sameOrigin test
            crossDomain: false, 
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type)) {
                    xhr.setRequestHeader("X-CSRFToken", get_csrf());
                }
            },
        });

        //globally configure ajax requests to redirect to login url when server returns unauthorized error
        $(document)
            .ajaxError(function(event, jqxhr, settings, exception) {
            if (jqxhr.status == 401) window.Router.navigate("login", {
                trigger: true
            });
        });

        //set the parent view - Applayout - containing the empty side and content panel
        $("#app")
            .empty()
            .append(AppLayout.el);
        AppLayout.render();
    };

    var get_csrf = function() {
        return $.cookie('csrftoken');
    };

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    };

    var update_appcache = function() {
        $(window)
            .load(function() {
            window.applicationCache.addEventListener('updateready', function(e) {
                if (window.applicationCache.status == window.applicationCache.UPDATEREADY) {
                    // Browser downloaded a new app cache.
                    // Swap it in and reload the page to get the new hotness.
                    window.applicationCache.swapCache();
                    if (confirm('A new version of this site is available. Load it?')) {
                        window.location.reload();
                    }
                }
            }, false);
        });
    };

    return {
        initialize: initialize
    };
});
