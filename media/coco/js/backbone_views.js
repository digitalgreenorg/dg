$(document).ready(function() {
    
    var village_list_view_configs = {'page_header':'Villages','backbone_collection': village_offline_collection,'table_template_name':'village_table_template', 'list_item_template_name':'village_list_item_template','add_edit_template_name':'screening_add_edit_template'};
    //var village_add_edit_view_configs = {'page_header':'Add Village','add_edit_template_name':'screening_add_edit_template'};
    var video_list_view_configs = {'page_header':'Videos','backbone_collection': video_offline_collection,'table_template_name':'video_table_template', 'list_item_template_name':'video_list_item_template'};
    var persongroup_list_view_configs = {'page_header':'Groups','backbone_collection': persongroup_offline_collection,'table_template_name':'persongroup_table_template', 'list_item_template_name':'persongroup_list_item_template'};
    var screening_list_view_configs = {'page_header':'Screenings','backbone_collection': screening_offline_collection,'table_template_name':'screening_table_template', 'list_item_template_name':'screening_list_item_template','add_edit_template_name':'screening_add_edit_template'};
    var person_list_view_configs = {'page_header':'Persons','backbone_collection': person_offline_collection,'table_template_name':'person_table_template', 'list_item_template_name':'person_list_item_template','add_edit_template_name':'person_add_edit_template'};       
    var personadoptvideo_list_view_configs = {'page_header':'Adoptions','backbone_collection': personadoptvideo_offline_collection,'table_template_name':'personadoptvideo_table_template' ,'list_item_template_name':'personadoptvideo_list_item_template'};        
    var animator_list_view_configs = {'page_header':'Animator','backbone_collection': animator_offline_collection,'table_template_name':'animator_table_template', 'list_item_template_name':'animator_list_item_template'};

    var HeaderView = Backbone.View.extend({
        // How many things to upload, button to go to the upload page
        // How many things to download, button to download
        // Name of the Current Page/View or maybe a breadcrumb
    })

    // UploadDownloadView
    // DashboardView
    // ListView -> search, add, table, sort
    // ListItemView -> add
    // AddEditView / AddView and EditView 


    // set up the view for a country
    var list_item_view = Backbone.View.extend({
        tagName: 'tr',
        events: {
            "click a.edit": "edit",
            "click a.destroy": "remove"
        },
        
        initialize: function(params){
            this.template= _.template($('#'+params.view_configs.list_item_template_name)
                .html());
        },
        
        edit: function(event) {
            event.preventDefault();
            event.stopImmediatePropagation();
            // call back up to the main app passing the current model for it
            // to allow a user to update the details
            list_view.edit(this.model);
        },

        remove: function(event) {
            event.stopImmediatePropagation();
            event.preventDefault();
            if (confirm("Are you sure you want to delete this entry?")) {
                this.model.remove();
            }
        },

       
        render: function() {
            $(this.el)
                .html(this.template(this.model.toJSON()));
            return this;
        }
    });
    
    var list_view = Backbone.View.extend({

        events: {
            "click button#add": "addNew",
            "click button#search_button": "search",
        },
        
        initialize: function(view_configs) {
            this.view_configs = view_configs;
            this.collection = new view_configs.backbone_collection();
            this.table_template_name = view_configs.table_template_name;
            console.log("template_name : "+this.table_template_name)
            this.template= _.template($('#'+'list_view_template').html());
            this.table_template =  _.template($('#'+this.table_template_name).html());
            this.collection.bind('all', this.render, this);
            this.collection.fetch();
        },
    
        render: function() {
            $(this.el)
                .html(this.template());
            $(this.el).append(this.table_template());
            $tbody = this.$("tbody");
            this.collection.each(function(model) {
                $tbody.append(new list_item_view({
                    model: model,view_configs: this.view_configs
                })
                    .render()
                    .el);
                     }, this);
            return this;
        },
        
        addNew: function() {
            console.log("add new");
            app.render_add_edit_view(this.view_configs);
        },
        edit: function(country) {
            console.log("edit: "+JSON.stringify(country.toJSON()));            
        },
        search: function() {

        }

    });

    var screening_add_edit_view = Backbone.View.extend({

        events: {
            'change #id_village': 'village_selection_changed'
            
        },
        
        initialize: function(view_configs) {
            
            this.view_configs = view_configs;
            console.log("temp name="+view_configs.add_edit_template_name)
            this.add_edit_template_name = view_configs.add_edit_template_name;
            this.add_edit_template =  _.template($('#'+this.add_edit_template_name).html());
            options_inner_template = _.template($('#options_template').html());
            this.villages = new village_offline_collection();
            this.videos = new video_offline_collection();
            this.persongroups = new persongroup_offline_collection();
            curr_village = null;
            _(this).bindAll('render_villages');
            _(this).bindAll('render_videos');
            _(this).bindAll('render_persongroups');
            
            this.villages.bind('all',this.render_villages);
            this.villages.fetch({success: function() {
                console.log("villages coll fetched");

            }});
            
            this.videos.bind('all',this.render_videos);
            this.videos.fetch({success: function() {
            console.log("videos coll fetched");

            }});    
            
            this.persongroups.bind('all',this.render_persongroups);
             // this.persongroups.fetch({success: function() {
             //            console.log("persongroups coll fetched");
             // 
             //            }});
        },
    
    
        village_selection_changed: function (e) {
            var value = $(e.currentTarget).val();
            curr_village=value;
            this.persongroups.fetch({
                    success: function() {
                    console.log("persongroups coll fetched");
                       }});
                       
            this.render_animators();
            console.log("village selected", value);
                
        },
            
        render: function() {
            $(this.el)
                .html(this.add_edit_template({villages:this.villages, options_inner_template: this.options_inner_template}));
            return this;
        },
        render_villages: function(){
            $village_list =this.$('#id_village');
            this.villages.each(function(village) {
                       $village_list.append(options_inner_template({id:village.get("id"),name:village.get("village_name")}));
                   });
        },
        render_animators: function(){
            $animator_list =this.$('#id_animator');
            vill = this.villages.where({id:curr_village})[0];
            console.log(vill);
            var animators = vill.get("animators");
            console.log(animators);
            console.log(typeof(animators));
            $.each(animators,function(index,animator) {
                       $animator_list.append(options_inner_template({id:animator.id,name:animator.name}));
                   });
        },
        render_videos: function(){
            $video_list =this.$('#id_videoes_screened');
            $video_list.html('');
            this.videos.each(function(video) {
                       $video_list.append(options_inner_template({id:video.get("id"),name:video.get("title")}));
                   });
        },
        render_persongroups: function(){
            // persongroups_for_village = this.persongroups.where({village['id']:curr_village});
            persongroups_for_village = this.persongroups.by_village(curr_village);
            console.log("filtered pg length= "+persongroups_for_village.length);
            $persongroup_list = this.$('#id_farmer_groups_targeted');
            $persongroup_list.html('');
            
            $.each(persongroups_for_village,function(index,persongroup) {
                       $persongroup_list.append(options_inner_template({id:persongroup.get("id"),name:persongroup.get("group_name")}));
                   });
        }
       
    });
    
    var person_add_edit_view = Backbone.View.extend({

        events: {
            'change #id_village': 'village_selection_changed'
            
        },
        
        initialize: function(view_configs) {
            
            this.view_configs = view_configs;
            this.add_edit_template_name = view_configs.add_edit_template_name;
            this.add_edit_template =  _.template($('#'+this.add_edit_template_name).html());
            options_inner_template = _.template($('#options_template').html());
            this.villages = new village_offline_collection();
            this.persongroups = new persongroup_offline_collection();
            curr_village = null;
            _(this).bindAll('render_villages');
            _(this).bindAll('render_persongroups');
            
            this.villages.bind('all',this.render_villages);
            this.villages.fetch({success: function() {
                console.log("villages coll fetched");

            }});
            
            
            this.persongroups.bind('all',this.render_persongroups);
             // this.persongroups.fetch({success: function() {
             //            console.log("persongroups coll fetched");
             // 
             //            }});
        },
    
    
        village_selection_changed: function (e) {
            var value = $(e.currentTarget).val();
            curr_village=value;
            this.persongroups.fetch({
                    success: function() {
                    console.log("persongroups coll fetched");
                       }});
                       
            console.log("village selected", value);
                
        },
            
        render: function() {
            $(this.el)
                .html(this.add_edit_template());
            return this;
        },
        render_villages: function(){
            $village_list =this.$('#id_village');
            this.villages.each(function(village) {
                       $village_list.append(options_inner_template({id:village.get("id"),name:village.get("village_name")}));
                   });
        },
        render_persongroups: function(){
            // persongroups_for_village = this.persongroups.where({village['id']:curr_village});
            persongroups_for_village = this.persongroups.by_village(curr_village);
            console.log("filtered pg length= "+persongroups_for_village.length);
            $persongroup_list = this.$('#id_group');
            $persongroup_list.html("<option value='' selected='selected'>---------</option> ");
            
            $.each(persongroups_for_village,function(index,persongroup) {
                       $persongroup_list.append(options_inner_template({id:persongroup.get("id"),name:persongroup.get("group_name")}));
                   });
        }
       
    });
    
    
    var HeaderView = Backbone.View.extend({
        //tagName:'tr',
        events: {

        },

        template: _.template($('#header')
            .html()),

        render: function(show_heading) {
            $(this.el)
                .html(this.template({
                header_name: show_heading
            }));
            return this;
        }
    });

    var DashboardView = Backbone.View.extend({
        //tagName:'tr',
        //this.model = conn_state,
        //this.model.bind('all', this.render, this);
        events: {
            "click button#connectivity": "toggle_connectivity",
            "click button#download": "Download",
            "click a.village": "list_village",
            "click a.video": "list_video",
            "click a.persongroup": "list_persongroup",
            "click a.screening": "list_screening",
            "click a.person": "list_person",
            "click a.personadoptvideo": "list_personadoptvideo",
            "click a.animator": "list_animator"
        },
        
        toggle_connectivity: function() {
            conn_state.set("connected", !conn_state.get("connected"));
            //Connected =!Connected;
            console.log("toggled connectivity");
            this.render();

        },

        fetch_save: function(collection_online, collection_offline, storeName) {
            var prevTime, curTime;
            curTime = (new Date())
                .getTime();
            prevTime = curTime;
            console.log("downloading  " + storeName);

            collection_online.fetch({
                success: function() {
                    data = (collection_online.toJSON());
                    console.log(storeName + " collection fetched ");
                    curTime = (new Date())
                        .getTime();
                    deltaTime = curTime - prevTime;
                    var download_time = deltaTime;
                    prevTime = curTime;
                    var db;
                    var request = indexedDB.open("coco-database");
                    request.onerror = function(event) {
                        console.log("Why didn't you allow my web app to use IndexedDB?!");
                    };
                    request.onsuccess = function(event) {
                        db = request.result;
                        //storeName="country";
                        var clearTransaction = db.transaction([storeName], "readwrite");
                        var clearRequest = clearTransaction.objectStore(storeName)
                            .clear();
                        clearRequest.onsuccess = function(event) {
                            console.log(storeName + ' objectstore cleared');
                            //collection_offline=new CountryCollection();
                            for (var i = 0; i < data.length; i++) {
                                // console.log("creating country "+JSON.stringify(data[i]));
                                collection_offline.create(data[i]);
                                //Do something
                            }

                            curTime = (new Date())
                                .getTime();

                            deltaTime = curTime - prevTime;
                            var writing_time = deltaTime;
                            console.log(storeName + " downloaded");
                            console.log(storeName + " downlaod time = " + download_time);
                            console.log(storeName + " writing time = " + writing_time);

                        };



                    }
                }
            });



        },

        Download: function() {
            console.log("starting download");
            //Download:fetch each model from server and save it to the indexeddb
            // countries_online = new CountryCollection_Online();
            // countries_offline = new CountryCollection();
            // this.fetch_save(countries_online, countries_offline, "country");

            villages_online = new village_online_collection();
            villages_offline = new village_offline_collection();
            this.fetch_save(villages_online, villages_offline, "village");

            videos_online = new video_online_collection();
            videos_offline = new video_offline_collection();
            this.fetch_save(videos_online, videos_offline, "video");

            persongroups_online = new persongroup_online_collection();
            persongroups_offline = new persongroup_offline_collection();
            this.fetch_save(persongroups_online, persongroups_offline, "persongroup");

            screenings_online = new screening_online_collection();
            screenings_offline = new screening_offline_collection();
            this.fetch_save(screenings_online, screenings_offline, "screening");

            persons_online = new person_online_collection();
            persons_offline = new person_offline_collection();
            this.fetch_save(persons_online, persons_offline, "person");

            personadoptvideos_online = new personadoptvideo_online_collection();
            personadoptvideos_offline = new personadoptvideo_offline_collection();
            this.fetch_save(personadoptvideos_online, personadoptvideos_offline, "personadoptvideo");

            animators_online = new animator_online_collection();
            animators_offline = new animator_offline_collection();
            this.fetch_save(animators_online, animators_offline, "animator");
        },

        list_village: function() {
            console.log("list village clicked");
            app.render_list_view(village_list_view_configs);
        },
        list_video: function() {
            console.log("list video clicked");
            app.render_list_view(video_list_view_configs);
        },
        list_persongroup: function() {
            console.log("list persongroup clicked");
            app.render_list_view(persongroup_list_view_configs);
        },
        list_screening: function() {
            console.log("list screening clicked");
            app.render_list_view(screening_list_view_configs);
        },
        list_person: function() {
            console.log("list person clicked");
            app.render_list_view(person_list_view_configs);
        },
        list_personadoptvideo: function() {
            console.log("list personadoptvideo clicked");
            app.render_list_view(personadoptvideo_list_view_configs);
        },
        list_animator: function() {
            console.log("list animator clicked");
            app.render_list_view(animator_list_view_configs);
        },

        template: _.template($('#dashboard')
            .html()),

        render: function() {
            var toggle_connectivity;

            if (conn_state.get("connected")) toggle_connectivity = "Offline";
            else toggle_connectivity = "Online";
            $(this.el)
                .html(this.template({
                toggle_connectivity: toggle_connectivity
            }));
            return this;
        }
    });

    var AppView = Backbone.View.extend({
        el: '#app',
        initialize: function() {
            header = new HeaderView();
            dashboard = new DashboardView({
                app: this
            });
            this.render();
        },
        render: function() {
            $(this.el)
                .append(header.render('Dashboard')
                .el);
            $(this.el)
                .append(dashboard.render()
                .el);
            return this;

        },
        render_list_view: function(view_configs) {
            $(this.el)
                .html('');
            $(this.el)
                .append(header.render(view_configs.page_header)
                .el);
            $(this.el)
                .append(new list_view(view_configs)
                .render()
                .el);
            return this;
        },
        render_add_edit_view: function(view_configs) {
            $(this.el)
                .html('');
            $(this.el)
                .append(header.render("Add "+view_configs.page_header)
                .el);
            if(view_configs.page_header=="Screenings")
            {
                current_add_edit_view = screening_add_edit_view
            }
            else if(view_configs.page_header=="Persons")
            {
                current_add_edit_view = person_add_edit_view
            }
            else
            {
                console.log("not screening");
                return this;
            }
            $(this.el)
                .append(new current_add_edit_view(view_configs)
                .render()
                .el);
            return this;
        }
        
    });

    var app = new AppView;


});
