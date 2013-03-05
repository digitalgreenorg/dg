define(['jquery', 'underscore', 'backbone', 'form_field_validator', 'syphon', 'views/notification', 'indexeddb_backbone_config', 'configs', 'views/form'
// Using the Require.js text! plugin, we are loaded raw text
// which will be used as our views primary template
// 'text!templates/project/list.html'
], function($, pas, pass, pass, pass, notifs_view, indexeddb, all_configs, Form) {


    var PersonAddEditView = Backbone.Layout.extend({

        initialize: function(params) {
            this.params = params;

        },
        template: "<div> <div id = 'form'></div> </div>",
        // views: {
        //     "#form": new new Form(this.options)
        //   },        
        beforeRender: function() {

            this.setView("#form", new Form(this.params));
            // this.render();
            // this.setView( "form",new Form(this.params));
            _(this)
                .bindAll('on_save');
            _(this)
                .bindAll('on_button2');
            $(document)
                .on("save_clicked", this.on_save);
            $(document)
                .on("button2_clicked", this.on_button2);


        },

        on_save: function(e) {
            e.stopPropagation();
            console.log("ADD/EDIT: Save clicked on form - ");
            console.log(e);
        },

        on_button2: function(e) {
            e.stopPropagation();
            console.log("ADD/EDIT: Button 2 clicked on form");
        }




    });

    // Our module now returns our view
    return PersonAddEditView;
});
