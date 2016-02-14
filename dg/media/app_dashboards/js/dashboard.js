/*Transaction class is an entry for a single transaction. It is a bunch that contains all the infromation required for a particular transaction*/
function Transaction(jsonObj) {
	/* Day of Transaction */
	this.day = jsonObj.selling.pickup.day;
	/* Farmer's name */
	this.farmer = jsonObj.selling.pickup.farmer.name;
	this.farmer_gender = jsonObj.selling.pickup.farmer.gender;

	/* Farmer's village */
	this.village = jsonObj.selling.pickup.farmer.village.village_name;

	/* Mediator's name */
	this.mediator = jsonObj.selling.pickup.mediator.name;
	/* Totol quantity of crop taken by the Mediator from the farmer */
	this.total_quantity = jsonObj.selling.quantity;
	/* Crop's name */
	this.crop = jsonObj.selling.crop.crop_name;
	/* Crop's measuring unit */
	this.unit = jsonObj.selling.crop.measuring_unit;
	/* Mandi's name in which the Mediator sold the crop */
	this.mandi = jsonObj.mandi.mandi_name;
	/* Quantity of the crop that mediator sold */
	this.quantity = jsonObj.quantity;
	/* Selling Price per unit of the crop at Mandi */
	this.price = jsonObj.selling_price;
	/* Total payment received by the farmer for this transaction */
	this.payment = jsonObj.selling.pickup.total_payment;
}

/* generates a contatenated string */
function concat(_1, _2) {
	return _1 + "-" + _2;
}
/* Aggregated Data Class */
function Aggregated_Info(name) {
	/* This can be a village name or mediator name */
	this.name = name;
	/* Total volume sold */
	this.total_volume = 0.0;
	/* Pay amount */
	this.pay_amount = 0.0;
	/* Active Farmers */
	this.active_farmers = 0.0;
	/* Average Farmers Per day */
	this.avg_farmers = 0.0;
}

Array.prototype.getUnique = function(){
	var u = {}, a = [];
	for(var i = 0, l = this.length; i < l; ++i){
		if(u.hasOwnProperty(this[i])) {
			 continue;
		}
		a.push(this[i]);
		u[this[i]] = 1;
	}
	return a;
}
/*Dashboard class is a collection of global datasets which should be readily available*/
function Dashboard() {
	var self = this;
	/*First we will populate the data based on the json which we will receive from ajax request*/
	/* Array containing all the transactions' data */
	this.transactions = [];
	/* Array of indexes depicting the transacitons which satisfy the input date range*/
	this.indexes = [];
	/* Start and end date variables */
	this.start_date = "";
	this.end_date = "";
	/* For all the fields below 'Active' refers to being within the query domain
	/* Set of All Farmers */
	this.farmers = {};
	/* Set of All Aggregators */
	this.aggregators = {};
	/* Set of All Crops */
	this.crops = {};
	/* Set of Active Mandis */
	this.mandis = {};
	/* Set of All Villages */
	this.villages = {};
	
	/* keeps name,total vol, total amt ,active_farmers list, avg farmers from start_date to end date*/
	/* Array of Village Aggregated Data Objects */
	this.village_info = [];
	/* Array of Mediator Aggregated Data Objects */
	this.mediator_info = [];
	/*list of active villages in that date range*/
	this.active_villages = [];
	/*list of mediators active in that date range*/
	this.active_mediators = [];
	
	/* Below are the set of helper data fields used in creating charts */
	/* List of days in the given date range */
	this.days = [];
	/* Day wise crop volume dictionary */
	this.crops_volume = {};
	/* Day wise crop weighted average price dictionary */
	this.crops_price = {};
	/* Day wise crop purchace dictionary */
	this.crops_purchase = {};
	/* Day wise number of farmers */
	this.farmers_count = [];
	/* Day wise Aggregator Crop Price Data */
	this.crop_aggregator_price = {};
	/* Day wise Aggregator Crop Volume Data */
	this.crop_aggregator_volume = {};

	/*list of active farmers in that date range*/



	this.populate_data = function populate_data_from_query(callback, callback2) {
		$.ajax({
			datatype: "json",
			url: "/api/v1/manditr/?limit=0&format=json"
			/*testing*/
			// url: "http://127.0.0.1:8000/api/v1/manditr/?limit=0&format=json&selling__pickup__day__gte=2015-12-10",
		}).done(function(data) {
			console.log(data);
			self.transactions = new Array(data.meta.total_count);
			self.indexes = [];
			var objects = data.objects;
			var length = objects.length;
			for (var i = 0; i < length; i++) {
				self.transactions[i] = new Transaction(objects[i]);
				self.indexes.push(i);
			}
			callback();
			callback2();
		});
	}
	this.initialize_filters = function() {
		/*This function creates the filters on UI*/
		/*It assumes that it has the list of all farmers, aggregators, crops and mandis*/
		initialize_farmers(self.farmers);
		initialize_aggregators(self.aggregators);
		initialize_crops(self.crops);
		initialize_mandis(self.mandis);
		self.log();
	}
	this.initialize_filter_data = function() {
		/*This function takes the indexes and initializes all farmers, aggregators, crops and mandis*/
		/*In this function we assume that the indexes are already filled and we will initialize the filters based on this*/
		self.farmers = {};
		self.aggregators = {};
		self.crops = {};
		self.mandis = {};
		for (var i = 0; i < self.indexes.length; i++) {
			var index = self.indexes[i];
			var transaction = self.transactions[index];
			if(i == 0) {
				self.start_date = transaction.day;
				self.end_date = transaction.day;
			} else {
				if(self.start_date > transaction.day)
					self.start_date = transaction.day;
				if(self.end_date < transaction.day)
					self.end_date = transaction.day;
			}
			self.farmers[transaction.farmer] = true;
			self.aggregators[transaction.mediator] = true;
			self.crops[transaction.crop] = true;
			self.mandis[transaction.mandi] = true;
		}
		self.initialize_filters();	
	}
	/* This function initializes the data structures relevant to the table creation in the dasboard page */
	this.aggregate_mediator_village_data = function() {
		/*get the unique mediators and mediator information*/

		var mediators = [];
		console.log("indexes", self.indexes);
		for (var i = 0; i < self.indexes.length; i++) {
			var index = self.indexes[i];
			var transaction = self.transactions[index];
			mediators.push(transaction.mediator);
		}
		var unique_mediators = mediators.getUnique();
		this.active_mediators = unique_mediators;
		self.mediator_info = [];
		for (var i=0; i < unique_mediators.length; i++) {
			self.mediator_info.push( {name:unique_mediators[i], total_volume: 0.0 , pay_amount: 0.0 , active_farmers: {} });
		}
		console.log(unique_mediators);
		for (var i = 0; i < self.indexes.length; i++) {
			var index = self.indexes[i];
			var transaction = self.transactions[index];
			var id = unique_mediators.indexOf(transaction.mediator);
			self.mediator_info[id].total_volume += transaction.quantity;
			self.mediator_info[id].pay_amount += transaction.payment;
			self.mediator_info[id].active_farmers[transaction.farmer]=true;
		}
		/*get the unique villages and village information*/
		var villages=[]; 
		var valid_transactions = []; /*to keep transactions corresponding to index array*/
		var valid_indexes = self.indexes;
	
		for (var i = 0; i < valid_indexes.length; i++) {
			valid_transactions.push(dashboard.transactions[valid_indexes[i]]);
			villages.push(dashboard.transactions[valid_indexes[i]].village);
		}
		self.active_villages = villages.getUnique();

		self.village_info=[]; /*To keep track of name,total_vol, pay, active farmers, avg farmer of all active villages*/
		for (var i = 0 ; i <self.active_villages.length; i++) {
			self.village_info.push({name:self.active_villages[i], total_volume: 0.0 , pay_amount: 0.0 , active_farmers: {} });
		}

		for (var i = 0; i < valid_transactions.length; i++) {
			var index = self.active_villages.indexOf(valid_transactions[i].village);
			self.village_info[index].total_volume += valid_transactions[i].quantity;
			self.village_info[index].pay_amount += valid_transactions[i].payment;
			self.village_info[index].active_farmers[valid_transactions[i].farmer]=true;
		}

	}

	this.aggregate_daywise_data = function() {
		/* This function initilizes all the data structures relevant to the charts creation in the dashboard page */
		self.days = [];
		self.crops_volume = {};
		self.crops_price = {};
		self.crops_purchase = {};
		self.crop_aggregator_price = {};
		self.crop_aggregator_volume = {};
		self.farmers_count = [];
		for(var i = 0; i < self.indexes.length; i++) {
			var index = self.indexes[i];
			var transaction = self.transactions[index];
			var id = $.inArray(transaction.day, self.days);
			
			if(id == -1) {
				/* Day not added in the list */
				self.days.push(transaction.day);
			}
			/* Here we will make set of aggregator crop tuples */
			tuple = concat(transaction.crop, transaction.mediator);
			self.crop_aggregator_price[tuple] = {};
			self.crop_aggregator_volume[tuple] = {};
			/*Set of Active Crops*/
			self.crops_price[transaction.crop] = {};
			self.crops_volume[transaction.crop] = {};
			self.crops_purchase[transaction.crop] = {};
		}
		/* Recievied the days list */
		/* Now initialize the data arrays */
		$.each(self.crops_price, function(key, value) {
			self.crops_volume[key] = new Array(self.days.length);
			self.crops_price[key] = new Array(self.days.length);
			self.crops_purchase[key] = new Array(self.days.length);
			var size = self.days.length;
			while(size--) {
				self.crops_volume[key][size] = 0;
				self.crops_price[key][size] = 0;
				self.crops_purchase[key][size] = 0;
			}
		});
		$.each(self.crop_aggregator_price, function(tuple, value) {
			self.crop_aggregator_price[tuple] = new Array(self.days.length);
			self.crop_aggregator_volume[tuple] = new Array(self.days.length);
			var size = self.days.length;
			while(size--) {
				self.crop_aggregator_price[tuple][size] = 0;
				self.crop_aggregator_volume[tuple][size] = 0;
			}
		});
		self.farmers_count = new Array(self.days.length);
		var size = self.days.length;
		while(size--) {
			self.farmers_count[size] = {};
		}

		/* Populate data */
		/* Crop prices are weighted averages. Therefore we will first calculate the income and then divide it by the total volume of the crop */
		for(var i = 0; i < self.indexes.length; i++) {
			var index = self.indexes[i];
			var transaction = self.transactions[index];
			var id = $.inArray(transaction.day, self.days);
			self.crops_price[transaction.crop][id] += transaction.quantity * transaction.price;
			self.crops_purchase[transaction.crop][id] += transaction.quantity * transaction.price;
			self.crops_volume[transaction.crop][id] += transaction.quantity;
			/*console.log(transaction.quantity);*/
			var tuple = concat(transaction.crop, transaction.mediator);
			self.crop_aggregator_price[tuple][id] += transaction.quantity * transaction.price;
			self.crop_aggregator_volume[tuple][id] += transaction.quantity;

			self.farmers_count[id][transaction.farmer] = true;
		}

		/* Normalizing crops_price and crop_aggregator_price and calculating farmer_counts */
		var size = self.days.length;
		while(size--) {
			self.farmers_count[size] = Object.keys(self.farmers_count[size]).length;
		}
		$.each(self.crops_price, function(key, value) {
			if (value) {
				var size = self.days.length;
				while(size--) {
					if(self.crops_volume[key][size] != 0)
						self.crops_price[key][size] /= self.crops_volume[key][size];
				}
			}
		});
		$.each(self.crop_aggregator_price, function(tuple, value) {
			var size = self.days.length;
			while(size--) {
				if(self.crop_aggregator_volume[tuple][size] !=0)
					self.crop_aggregator_price[tuple][size] /= self.crop_aggregator_volume[tuple][size];
			}
		});
	}
	this.log = function() {
		console.log(self);
	}
}
	
