// The client agent to communicate with backends to process authentication requests
// Exports an interface providng 3 methods - login, logout, check_login - for login view to use
// Based on internet-connectivity, it runs the authentication requests against the - server and the offline backend
define([
    'models/user_model',
    'auth_offline_backend',
    'configs',
    'offline_utils',
    'jquery_cookie'
], function(User, OfflineAuthBackend, all_configs, Offline) {

    var internet_connected = function() {
        return navigator.onLine;
    }

    // checks whether the user is logged in or not in both backends- based on internet connectivity 
    var check_login = function() {
        var dfd = new $.Deferred()
        console.log("checking login");
        if (check_online_login()) {
            OfflineAuthBackend.check_login()
                .done(function() {
                    dfd.resolve();
                })
                .fail(function(error) {
                    dfd.reject(error);
                });
        } else {
            dfd.reject("Not logged in on server");
        }
        return dfd.promise();
    }

    
    //ideally shd have been exacty same as the server uses. But approximating it to avoid network request.
    var check_online_login = function() {
        if (!internet_connected || $.cookie('sessionid'))
            return true;
        return false;
    }
    
    // logs out of the offline backend, if internet accessible- logs out of the server backend
    var logout = function() {
        var dfd = new $.Deferred();
        var that = this;
        online_logout()
            .always(function() {
                OfflineAuthBackend.logout()
                    .always(function() {
                        dfd.resolve();
                    })
            });
        return dfd;
    }
    
    // logs out of the online backend if internet accessible
    var online_logout = function() {
        var dfd = new $.Deferred();

        if (!internet_connected())
            dfd.resolve();
            
        // the logout endpoint should be made configurable
        $.post("/coco/logout/")
            .done(function(resp) {
                return dfd.resolve();
            })
            .fail(function(resp) {
                return dfd.reject(resp);
            });

        return dfd.promise();
    }
    
    // logs-in to the offline backend, if internet accessible - logs-in to the server backend
    var login = function(username, password) {
        var dfd = new $.Deferred();
        console.log("Attemting login");
        // internet accessible - login to server backend - when successfull - login to offline backend
        if (internet_connected()) {
            // try server backend login
            online_login(username, password)
                .fail(function(error) {
                    console.log("Online login failed - " + error);
                    dfd.reject(error);
                })
                .done(function() {
                    // online login successful, try offline backend login
                    OfflineAuthBackend.login(username, password)
                        .done(function() {
                            // login successful
                            console.log("Login Successful");
                            post_login_success();
                            dfd.resolve();
                        })
                        .fail(function (error){
                            console.log("Offline login failed - " + error);
                            dfd.reject(error);
                        });
                });
        } else {
            // internet not accessible - only try logging into offline backend
            OfflineAuthBackend.login(username, password)
                .done(function() {
                    console.log("Login Successful");
                    post_login_success();
                    dfd.resolve();
                })
                .fail(function (error) {
                    console.log("Offline login failed - " + error);
                    dfd.reject(error);
                });
        }
        return dfd;
    }
    
    // run any onLogin logic defined by user
    var post_login_success = function (){
        if (all_configs.misc.onLogin)
            all_configs.misc.onLogin(Offline, this);
            return;
    }

    // resolves if server returns 1 or internet is not connected otherwise rejects
    var online_login = function(username, password) {
        var dfd = new $.Deferred();
        if (!internet_connected())
            return dfd.resolve();
        //the endpoint should be made configurable     
        $.post("/coco/login/", {
            "username": username,
            "password": password
        })
            .done(function(resp) {
                if (resp == "1")
                    return dfd.resolve();
                else
                    return dfd.reject("Username or password is incorrect (Server)");
            })
            .fail(function(resp) {
                return dfd.reject("Could not contact server. Try again in a minute.");
            });
        return dfd.promise();
    }
    
    return {
        check_login: check_login,
        logout: logout,
        login: login
    };
});
