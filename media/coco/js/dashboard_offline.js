$(function() {
	var Connectivity = Backbone.Model.extend({
		defaults: function() {
			return {
				connected: false
			};
		}
	});

	conn_state = new Connectivity();
	var databasev1 = {
		id: "coco-database",
		description: "The offline database for COCO",
		migrations: [{
			version: 1,
			migrate: function(transaction, next) {
				transaction.db.createObjectStore("country", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("village", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("video", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("persongroup", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("screening", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("person", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("personadoptvideo", {
					autoIncrement: true
				});
				transaction.db.createObjectStore("animator", {
					autoIncrement: true
				});
				console.log("created")
				//store.createIndex("nameIndex", "country_name", { unique: false })
				next();
			}
		}]
	};

	// country model
	var Country = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "country",

	});

	var Country_Online = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/country/' + this.id + "/" : '/api/v1/country/?limit=0';
		}

	});
	var CountryCollection_Online = Backbone.Collection.extend({
		model: Country_Online,
		url: '/api/v1/country/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	// define the collection of countries
	var CountryCollection = Backbone.Collection.extend({
		model: Country,
		database: databasev1,
		storeName: "country",
	});

	var village_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "village",

	});

	var village_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/village/' + this.id + "/" : '/api/v1/village/?limit=0';
		}

	});
	var village_online_collection = Backbone.Collection.extend({
		model: village_online_model,
		url: '/api/v1/village/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	// define the collection of countries
	var village_offline_collection = Backbone.Collection.extend({
		model: village_offline_model,
		database: databasev1,
		storeName: "village",
	});



	var video_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "video",

	});

	var video_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/video/' + this.id + "/" : '/api/v1/video/?limit=0';
		}

	});
	var video_online_collection = Backbone.Collection.extend({
		model: video_online_model,
		url: '/api/v1/video/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var video_offline_collection = Backbone.Collection.extend({
		model: video_offline_model,
		database: databasev1,
		storeName: "video",
	});

	var persongroup_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "persongroup",

	});

	var persongroup_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/persongroup/' + this.id + "/" : '/api/v1/persongroup/?limit=0';
		}

	});
	var persongroup_online_collection = Backbone.Collection.extend({
		model: persongroup_online_model,
		url: '/api/v1/persongroup/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var persongroup_offline_collection = Backbone.Collection.extend({
		model: persongroup_offline_model,
		database: databasev1,
		storeName: "persongroup",
	});

	var screening_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "screening",

	});

	var screening_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/screening/' + this.id + "/" : '/api/v1/screening/?limit=0';
		}

	});
	var screening_online_collection = Backbone.Collection.extend({
		model: screening_online_model,
		url: '/api/v1/screening/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var screening_offline_collection = Backbone.Collection.extend({
		model: screening_offline_model,
		database: databasev1,
		storeName: "screening",
	});


	var person_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "person",

	});

	var person_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/person/' + this.id + "/" : '/api/v1/person/?limit=0';
		}

	});
	var person_online_collection = Backbone.Collection.extend({
		model: person_online_model,
		url: '/api/v1/person/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var person_offline_collection = Backbone.Collection.extend({
		model: person_offline_model,
		database: databasev1,
		storeName: "person",
	});

	var personadoptvideo_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "personadoptvideo",

	});

	var personadoptvideo_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/personadoptvideo/' + this.id + "/" : '/api/v1/personadoptvideo/?limit=0';
		}

	});
	var personadoptvideo_online_collection = Backbone.Collection.extend({
		model: personadoptvideo_online_model,
		url: '/api/v1/personadoptvideo/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var personadoptvideo_offline_collection = Backbone.Collection.extend({
		model: personadoptvideo_offline_model,
		database: databasev1,
		storeName: "personadoptvideo",
	});

	var animator_offline_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		database: databasev1,
		storeName: "animator",

	});

	var animator_online_model = Backbone.Model.extend({
		remove: function() {
			this.destroy();
		},
		sync: Backbone.ajaxSync,
		url: function() {
			return this.id ? '/api/v1/animator/' + this.id + "/" : '/api/v1/animator/?limit=0';
		}

	});
	var animator_online_collection = Backbone.Collection.extend({
		model: animator_online_model,
		url: '/api/v1/animator/?limit=0',
		sync: Backbone.ajaxSync,
		parse: function(data) {
			return data.objects;
		}

	});

	var animator_offline_collection = Backbone.Collection.extend({
		model: animator_offline_model,
		database: databasev1,
		storeName: "animator",
	});


	// set up the view for a country
	var CountryView = Backbone.View.extend({
		tagName: 'tr',
		events: {
			"click a.edit": "editCountry",
			"click a.destroy": "remove"
		},

		editCountry: function(event) {
			event.preventDefault();
			event.stopImmediatePropagation();
			// call back up to the main app passing the current model for it
			// to allow a user to update the details
			this.options.handle.editCountry(this.model);
		},

		remove: function(event) {
			event.stopImmediatePropagation();
			event.preventDefault();
			if (confirm("Are you sure you want to delete this entry?")) {
				this.model.remove();
			}
		},

		template: _.template($('#tpl-country-item').html()),

		render: function() {
			$(this.el).html(this.template(this.model.toJSON()));
			return this;
		}
	});



	var CountriesView = Backbone.View.extend({
		//tagName:'tr',
		initialize: function() {
			// instantiate a country collection
			//console.log(conn_state);
			if (conn_state.get("connected")) {
				console.log("We are online");
				this.countries = new CountryCollection_Online();
			} else {
				console.log("We are offline");
				this.countries = new CountryCollection();
			}
			this.countries.bind('all', this.render, this);
			this.countries.fetch();
		},
		events: {

		},

		template: _.template($('#countries_table').html()),
		render: function() {
			$(this.el).html(this.template());
			this.countries.each(function(country) {
				$(this.el).find('tbody').append(new CountryView({
					model: country,
					handle: this.options.handle
				}).render().el);
			}, this);
			return this;
		}
	});

	var CountryListPage = Backbone.View.extend({

		events: {
			"click button#add": "addCountry",
			"click button#search_button": "searchCountry",
			"click #countryForm :submit": "handleModal",
			"keydown #countryForm": "handleModalOnEnter",
			"hidden #countryModal": "prepareForm"
		},
		initialize: function() {
			// instantiate a country collection
			this.countries_view = new CountriesView({
				handle: this
			});
		},
		template: _.template($('#country_list_page').html()),
		render: function() {
			$(this.el).html(this.template());
			$(this.el).append(this.countries_view.render().el);
			return this;
		},
		addCountry: function(event) {
			//alert("add ");
			event.stopImmediatePropagation();
			event.preventDefault();
			this.prepareForm(null);
			$('#countryModal').modal('show');

		},
		addNew: function(country) {
			//alert(country);
			//alert(JSON.stringify(country));
			this.countries_view.countries.create(country, {
				wait: true
			});

		},
		editCountry: function(country) {
			//alert("edit "+JSON.stringify(country));
			this.prepareForm(country.toJSON());
			$('#countryModal').data('countryId', country.get('id'));
			$('#countryModal').modal('show');
		},
		prepareForm: function(countryData) {
			countryData = countryData || {};

			var data = {
				'country_name': '',
				'start_date': ''
			};

			$.extend(data, countryData);

			var form = $('#countryForm');
			$(form).find('#id_country_name').val(data.country_name);
			$(form).find('#id_start_date').val(data.start_date);
			// clear any previous references to countryId in case the user
			// clicked the cancel button
			$('#countryModal').data('countryId', '');
		},

		handleModal: function(event) {
			event.preventDefault();
			event.stopImmediatePropagation();
			var form = $('#countryForm');

			var countryData = {
				country_name: $(form).find('#id_country_name').val(),
				start_date: $(form).find('#id_start_date').val(),
			};

			if ($('#countryModal').data('countryId')) {
				countryData.id = $('#countryModal').data('countryId');
				this.updateCountry(countryData);
			} else {
				// add or update the country
				this.addNew(countryData);
			}

			// hide the modal
			$('#countryModal').modal('hide');

			return this;
		},

		handleModalOnEnter: function(event) {
			// process the modal if the user pressed the ENTER key
			if (event.keyCode == 13) {
				return this.handleModal(event);
			}
		},

		updateCountry: function(countryData) {
			var country = this.countries_view.countries.get(countryData.id)
			if (_.isObject(country)) {
				// iterate through all the data in countryData, setting it
				// to the country model
				for (var key in countryData) {
					// ignore the ID attribute
					if (key != 'id') {
						country.set(key, countryData[key]);
					}
				}

				// persist the change
				country.save({
					wait: true
				});
			}


		},

		searchCountry: function() {

			//alert($('#search_box').val());
			this.countries_view.countries.fetch({
				conditions: {
					country_name: $('#search_box').val()
				},
				success: function() {
					// The theater collection will be populated with all the movies whose genre is "adventure"
				}
			});
		}



	});




	var HeaderView = Backbone.View.extend({
		//tagName:'tr',
		events: {

		},

		template: _.template($('#header').html()),

		render: function(show_heading) {
			$(this.el).html(this.template({
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
			"click button#connectivity": "ToggleConnectivity",
			"click button#download": "Download",
			"click a.country": "ListCountry",
			"click a.state": "ListState",
			"click a.district": "ListDistrict",
			"click a.block": "ListBlock",
			"click a.village": "ListVillage"

		},
		ToggleConnectivity: function() {
			conn_state.set("connected", !conn_state.get("connected"));
			//Connected =!Connected;
			console.log("toggled connectivity");
			this.render();

		},

		Fetch_Save: function(collection_online, collection_offline, storeName) {
			var prevTime, curTime;
			curTime = (new Date()).getTime();
			prevTime = curTime;
			console.log("downloading  " + storeName);

			collection_online.fetch({
				success: function() {
					data = (collection_online.toJSON());
					console.log(storeName + " collection fetched ");
					curTime = (new Date()).getTime();
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
						var clearRequest = clearTransaction.objectStore(storeName).clear();
						clearRequest.onsuccess = function(event) {
							console.log(storeName + ' objectstore cleared');
							//collection_offline=new CountryCollection();
							for (var i = 0; i < data.length; i++) {
								// console.log("creating country "+JSON.stringify(data[i]));
								collection_offline.create(data[i]);
								//Do something
							}

							curTime = (new Date()).getTime();

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
			countries_online = new CountryCollection_Online();
			countries_offline = new CountryCollection();
			this.Fetch_Save(countries_online, countries_offline, "country");

			villages_online = new village_online_collection();
			villages_offline = new village_offline_collection();
			this.Fetch_Save(villages_online, villages_offline, "village");

			videos_online = new video_online_collection();
			videos_offline = new video_offline_collection();
			this.Fetch_Save(videos_online, videos_offline, "video");

			persongroups_online = new persongroup_online_collection();
			persongroups_offline = new persongroup_offline_collection();
			this.Fetch_Save(persongroups_online, persongroups_offline, "persongroup");

			screenings_online = new screening_online_collection();
			screenings_offline = new screening_offline_collection();
			this.Fetch_Save(screenings_online, screenings_offline, "screening");
		
			persons_online = new person_online_collection();
			persons_offline = new person_offline_collection();
			this.Fetch_Save(persons_online, persons_offline, "person");

			personadoptvideos_online = new personadoptvideo_online_collection();
			personadoptvideos_offline = new personadoptvideo_offline_collection();
			this.Fetch_Save(personadoptvideos_online, personadoptvideos_offline, "personadoptvideo");

			animators_online = new animator_online_collection();
			animators_offline = new animator_offline_collection();
			this.Fetch_Save(animators_online, animators_offline, "animator");
		},

		ListCountry: function() {
			this.options.app.renderListCountry();
			//new CountryListPage().render();
		},
		ListState: function() {

		},
		ListDistrict: function() {

		},
		ListBlock: function() {

		},
		ListVillage: function() {

		},

		template: _.template($('#dashboard').html()),

		render: function() {
			var toggle_connectivity;

			if (conn_state.get("connected")) toggle_connectivity = "Offline";
			else toggle_connectivity = "Online";
			$(this.el).html(this.template({
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
			$(this.el).append(header.render('Dashboard').el);
			$(this.el).append(dashboard.render().el);
			return this;

		},
		renderListCountry: function() {
			$(this.el).html('');
			$(this.el).append(header.render('Countries').el);
			$(this.el).append(new CountryListPage().render().el);
			return this;
		}
	});

	var app = new AppView;


});
