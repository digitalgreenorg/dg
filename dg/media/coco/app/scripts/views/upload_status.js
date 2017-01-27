//this view displays upload status of collections in upload_q i.e. number of enteries uploaded and are pending to be uploaded, when connection with server is aborted
define([
    'jquery',
    'underscore',
    'layoutmanager',
    'collections/upload_collection',
    'models/user_model',
    'configs'
    ], function(jquery, underscore, layoutmanager, upload_collection, User, configs) {

        var UploadStatusView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new upload status view");
             _(this).bindAll('tear_down');
        },

        template: "#upload_status_template",

        events: {
            "click #Ok": "tear_down"
        },
        
        serialize: function () {
            //send these to the list page template
            var language = User.get('language');
            return {
                language: language,
                configs: configs,
            };
        },

        //removes the view
        tear_down: function() {
            $('#upload_status_modal').modal('hide');
            $('.modal-backdrop').remove();
        },

        //update the status on the view 
        update_total: function(total) {
            $('#upl_total').html(total);
        },

        update_done: function(uploaded){
            $('#upl_done').html(uploaded);
        },

        update_pending: function(pending){
            $('#upl_pending').html(pending);
        },

        //feeds data to template
        get_status: function(total, uploaded, pending) {
            this.update_total(total);
            this.update_done(uploaded);
            this.update_pending(pending);
        }

    });

    // Our module now returns our view
    return UploadStatusView;
});
