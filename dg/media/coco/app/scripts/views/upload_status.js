define([
    'jquery',
    'underscore',
    'layoutmanager',
    'collections/upload_collection',
    ], function(jquery, underscore, layoutmanager, upload_collection) {

        var UploadStatusView = Backbone.Layout.extend({

        initialize: function() {
            console.log("UPLOAD: initializing new upload view");
            _.bindAll(this);
        },

        template: "#upload_status_template",

        events: {
            "click #Ok": "tear_down"
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
            $('upl_pending').html(pending);
        },

        get_status: function(total, uploaded, pending) {
            this.update_total(total);
            this.update_done(uploaded);
            this.update_pending(pending);
        }

    });



    // Our module now returns our view
    return UploadStatusView;
});
