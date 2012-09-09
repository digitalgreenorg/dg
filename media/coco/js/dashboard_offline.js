$(function(){

  var HeaderView = Backbone.View.extend({
                                         //tagName:'tr',
                                             events: {
                                             
                                             },
                                             
                                             template:_.template($('#header').html()),
                                             
                                             render: function (show_heading) {
                                                 $(this.el).html(this.template({header_name:show_heading}));
                                                 return this;
                                             }
                                         });

  var DashboardView = Backbone.View.extend({
                                        //tagName:'tr',
                                            events: {
                                               "click a.country" : "ListCountry",
                                               "click a.state" : "ListState",
                                                "click a.district" : "ListDistrict",
                                                "click a.block" : "ListBlock",
                                                "click a.village" : "ListVillage"
                                           
                                            },
                                           
                                           ListCountry: function() {
                                                alert("in country listing");
                                           },
                                           ListState: function() {
                                           
                                           },
                                           ListDistrict: function() {
                                           
                                           },
                                           ListBlock: function() {
                                           
                                           },
                                           ListVillage: function() {
                                           
                                           },
                                            
                                           template:_.template($('#dashboard').html()),
                                            
                                            render: function () {
                                                $(this.el).html(this.template());
                                                return this;
                                            }
                                        });

  
  var AppView = Backbone.View.extend({
                                        el:'#app',

                                        initialize: function() {
                                             header = new HeaderView();
                                            dashboard= new DashboardView();
                                             this.render();
                                        },
                                        render:function(){
                                            $(this.el).append(header.render('Dashboard').el);
                                            $(this.el).append(dashboard.render().el);
                                            return this;
                                     
                                     }
  });
  
  var app = new AppView;

  
  });