define(['jquery', 'underscore', 'backbone', 'configs', 'indexeddb_backbone_config', 'views/form', 'indexeddb-backbone','collections/upload_collection','views/upload', 'views/incremental_download'], function($, pass, pass, configs, indexeddb, Form, pass, upload_collection, UploadView,IncDownloadView) {

    var DashboardView = Backbone.Layout.extend({
        template: "#dashboard",
        events: {
            // "click button#download": "Download",
            "click #sync": "upload",
            "click #inc_download": "inc_download",
                
        },

        item_template: _.template($("#dashboard_item_template")
            .html()),
        initialize: function() {
            this.upload_v = null;
            this.inc_download_v = null;
        },

        afterRender: function() { /* Work with the View after render. */
            // this.collection.fetch();
            for (var member in configs) {
                // console.log(configs[member]);
                $('#dashboard_items')
                    .append(this.item_template({
                    name: member,
                    title: configs[member]["page_header"]
                }));
                $('#dashboard_items_add')
                    .append(this.item_template({
                    name: member+"/add",
                    title: '<i class="icon-plus-sign"></i>'
                }));
                    

            }
        },
        
        upload: function(){
            if(!this.upload_v){
                console.log("DASHBIARD: creating new upload view"); 
                this.upload_v = new UploadView();
            }
            this.setView("#upload_modal_ph",this.upload_v);
            this.render();
            this.upload_v.start_upload();
            // var up_v = new UploadView();
//             if(this.getView("#upload_modal_ph"))
//                 {
//                     alert("view r");
//                     this.removeView("#upload_modal_ph");
//                 }
//             this.setView("#upload_modal_ph",up_v);
//             this.render();
//             up_v.start_upload();

        },
            
        inc_download: function(){
            if(!this.inc_download_v)
            {
                this.inc_download_v = new IncDownloadView();
            }
            this.setView("#upload_modal_ph",this.inc_download_v);
            this.render();
            this.inc_download_v.start_incremental_download();
            
            
        }        

        
    });


    // Our module now returns our view
    return DashboardView;
});
