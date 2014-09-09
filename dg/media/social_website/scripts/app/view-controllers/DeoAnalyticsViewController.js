/**
 * CollectionAddEditController Class File
 *
 * @author aadish
 * @version $Id$
 * @requires require.js
 * @requires jQuery
 */

define(function(require) {
    'use strict';
    var Controller = require('framework/controllers/Controller');
    var viewRenderer = require('framework/ViewRenderer');
    var jQuery = require('jquery');
    var Select2 = require('libs/external/select2');
    var HighChart = require('libs/external/highcharts');
    
    var DistrictDataFeed = require('app/libs/DistrictDataFeed');
    var DeoDataFeed = require('app/libs/DeoDataFeed');
    
    var districtTemplate = require('text!app/views/district.html');
    var deoTemplate = require('text!app/views/deo.html');
    var deoTabTemplate = require('text!app/views/deo_name_tab.html');
    
    var DeoAnalyticsViewController = Controller.extend({

        /**
         * Controller constructor
         * @return {Controller} this
         */
        constructor: function($referenceBase) {
            this.base($referenceBase);
            this.initSelect2();
            return this;
        },

        _initReferences: function($referenceBase) {
            this.base();
            var references = this._references;
            references.districtdataFeed = new DistrictDataFeed();
            references.deodataFeed = new DeoDataFeed();
            references.$analyticsWrapper = $referenceBase;
            references.$districtContainer = $referenceBase.find('.js-district-container');
            references.$deoContainer = $referenceBase.find('.js-deo-container');
            references.$deoTabContainer = $referenceBase.find('.js-deo-tab-container');
            references.$goButton = $referenceBase.find('.js-go-btn');
            references.$dayTab = $referenceBase.find('.js-daily-tab');
            references.$weekTab = $referenceBase.find('.js-weekly-tab');
            references.$monthTab = $referenceBase.find('.js-monthly-tab');
            references.$prevPointer = $referenceBase.find('.js-prev-pointer');
            references.$nextPointer = $referenceBase.find('.js-next-pointer');
            references.$partnerList = $referenceBase.find('.js-partnerlist');
        },

        _initEvents: function() {
            this.base();
            var boundFunctions = this._boundFunctions;
            var references = this._references;
            
            boundFunctions.onDistrictDataProcessed = this._onDistrictDataProcessed.bind(this);
            references.districtdataFeed.on('dataProcessed', boundFunctions.onDistrictDataProcessed);
            
            boundFunctions.onDeoDataProcessed = this._onDeoDataProcessed.bind(this);
            references.deodataFeed.on('dataProcessed', boundFunctions.onDeoDataProcessed);
            
            boundFunctions.onGoBtnClick = this._onGoBtnClick.bind(this);
            references.$goButton.on("click", boundFunctions.onGoBtnClick);
            
            boundFunctions.onDayTabClick = this._onDayTabClick.bind(this);
            references.$dayTab.on("click", boundFunctions.onDayTabClick);
            
            boundFunctions.onWeekTabClick = this._onWeekTabClick.bind(this);
            references.$weekTab.on("click", boundFunctions.onWeekTabClick);
            
            boundFunctions.onMonthTabClick = this._onMonthTabClick.bind(this);
            references.$monthTab.on("click", boundFunctions.onMonthTabClick);
            
            boundFunctions.onPrevPointerClick = this._onPrevPointerClick.bind(this);
            references.$prevPointer.on("click", boundFunctions.onPrevPointerClick);
            
            boundFunctions.onNextPointerClick = this._onNextPointerClick.bind(this);
            references.$nextPointer.on("click", boundFunctions.onNextPointerClick);
            
            boundFunctions.onPartnerChosen = this._onPartnerChosen.bind(this);
            references.$partnerList.on('change', this._boundFunctions.onPartnerChosen);
            
        },
        
        setDate: function(counter, d)
        {
            var references = this._references
            if (counter == -1)
            {
                d.setDate(d.getDate() - 1);
            }
            else
            {
                if (counter == 1)  
                {
                    d.setDate(d.getDate() + 1);
                }
            }
           
            var dd = d.getDate();
           
            references.days = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
            references.months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

            var day = references.days[d.getDay()];
            var mon = references.months[d.getMonth()];
            var yyyy = d.getFullYear();

            if(dd<10) {dd='0'+dd} 

            d = day+' '+ dd+' '+mon+' '+yyyy;
            jQuery("div#dateshow").html(d);
        },
        
        setWeekSingleDate: function(d)
        {
          var day = d.getDay();

          var startweek = new Date(d);
          var endweek = new Date(d);
          
          if (day == 0) {startweek.setDate(d.getDate() - 6); endweek.setDate(d.getDate());}
          else if (day == 1) {startweek.setDate(d.getDate()); endweek.setDate(d.getDate() + 6);}
          else if (day == 2) {startweek.setDate(d.getDate() - 1); endweek.setDate(d.getDate() + 5);}
          else if (day == 3) {startweek.setDate(d.getDate() - 2); endweek.setDate(d.getDate() + 4);}
          else if (day == 4) {startweek.setDate(d.getDate() - 3); endweek.setDate(d.getDate() + 3);}
          else if (day == 5) {startweek.setDate(d.getDate() - 4); endweek.setDate(d.getDate() + 2);}
          else if (day == 6) {endweek.setDate(d.getDate() + 1); startweek.setDate(d.getDate() - 5);}
          
          this.setWeekTwoDates(0, startweek, endweek);
        },
        
        setWeekTwoDates: function(counter, startweek, endweek)
        {
            var references = this._references  
            if (counter == -1)  {startweek.setDate(startweek.getDate() - 7); endweek.setDate(endweek.getDate() - 7);}
            else if (counter == 1)  {startweek.setDate(startweek.getDate() + 7); endweek.setDate(endweek.getDate() + 7);}
           
            var startweekmon = references.months[startweek.getMonth()];
            var endweekmon = references.months[endweek.getMonth()];
         
            var yrstartweek = startweek.getFullYear();
            var yrendweek = endweek.getFullYear();

            var d = startweek.getDate()+ ' ' + startweekmon + ' ' + yrstartweek + '-'+ endweek.getDate() +' '+ endweekmon + ' '+ yrstartweek;  

            $("div#dateshow").html(d);    
        },
        
        setMonthDate: function(d)
        {
            var references = this._references;
            var mon = references.months[d.getMonth()];
            
            var yyyy = d.getFullYear();

            d = mon +' '+ yyyy;
            $("div#dateshow").html(d);
        },
        
        getScreenDate: function(cn)
        {
            var references = this._references;
            var userdate = jQuery('#dateshow').html();; 
            var datesplitted = userdate.split(" ");

            var dd = datesplitted[1];
           
            var yyyy = datesplitted[3];
            var mm = references.months.indexOf(datesplitted[2]);
       
            if (cn == 2) {mm = mm+1}
            if(mm<10) {mm='0'+mm}
       
            var dateformatted;
            if (cn==1)
             {
               dateformatted = new Date (yyyy, mm, dd);        
             }
            else if (cn == 2)
             {
               dateformatted = yyyy+'-'+mm+'-'+dd;
             }
            else if (cn == 3)
             {
               dateformatted = new Date (yyyy, mm, dd);
               dateformatted.setDate(dateformatted.getDate() + 1);
               
               yyyy = dateformatted.getFullYear();
               mm = dateformatted.getMonth() + 1;
               if(mm<10) {mm='0'+mm}
               dd = dateformatted.getDate();
               
               dateformatted = yyyy+'-'+mm+'-'+dd;
             }
            return dateformatted;
        },
        
        getScreenWeekDate: function(cn, rdate)
        {
            var references = this._references
            var date = rdate.split(" ");
           
            var dd = date[0];       
            var yyyy = date[2];
            var mm = references.months.indexOf(date[1]);
            if (cn == 2) {mm = mm+1}
            if(mm<10) {mm='0'+mm}
       
            var dateformatted;
            if (cn==1)
            {
               dateformatted = new Date (yyyy, mm, dd);        
            }
            else if (cn == 2)
            {
               dateformatted = yyyy+'-'+mm+'-'+dd;
            }  
            return dateformatted;
        },
        
        getMonthFirstDate: function(cn)
        {
            var references = this._references
            var data = jQuery('#dateshow').html();
            var usermonth = data.split(" ");
           
            var d = new Date (usermonth[1], references.months.indexOf(usermonth[0]), '01');
           
            if (cn == 2)
            {
                var mm = d.getMonth() + 1;
                d = d.getFullYear()+'-'+mm+'-'+d.getDate();
            }   
            return d;
        },
        
        getMonthLastDate: function()
        {
            var d = this.getMonthFirstDate(1);
            
            var ld = new Date(d.getFullYear(), d.getMonth()+1, 0);
            
            var ldmm = ld.getMonth() + 1;
            var ld = ld.getFullYear()+'-'+ldmm+'-'+ld.getDate();
            
            return ld;
            
        },
        
        setDay: function()
        {
            var references = this._references
            var userdate = jQuery('#dateshow').html();
            var first = userdate.split(" ");

            if (first[0] == parseInt(first[0])) //coming to DAILY view from WEEKLY view
            {
                var dates = userdate.split("-");
                var date1 = this.getScreenWeekDate(1, dates[0]);        
                this.setDate(0, date1);
            }
            else if (jQuery.inArray(first[0], references.months) >= 0) 
                //coming to DAILY from MONTHLY              
            {
                var d = this.getMonthFirstDate(1);
                
                var dayofweek = references.days[d.getDay()];
                var mon = references.months[d.getMonth()];
                
                d = dayofweek+' '+ d.getDate() +' '+mon+' '+d.getFullYear();
                $("div#dateshow").html(d);          
            }
            //analyzedeo();
        },
        
        setWeek: function()
        {
            var references = this._references
            var userdate = jQuery('#dateshow').html();
            var first = userdate.split(" ");
           
            if (jQuery.inArray(first[0], references.days) >= 0) //coming to WEEKLY view from DAILY view      
            {
                var mydate = this.getScreenDate(1);    
                this.setWeekSingleDate(mydate);
            }
            else if ((jQuery.inArray(first[0], references.months) >= 0)) //coming to WEEKLY from MONTHLY view
            {
               var d = this.getMonthFirstDate(1);     
               this.setWeekSingleDate(d);
            }
            //analyzedeo();
        },
        
        setMonth: function()
        {
            var references = this._references
            var userdate = jQuery('#dateshow').html();
            var first = userdate.split(" ");

            if ((jQuery.inArray(first[0], references.days) >= 0)) //coming to MONTHLY view from DAILY view
            {
                var mydate = this.getScreenDate(1);
                this.setMonthDate(mydate);
            }
            else if (first[0] == parseInt(first[0])) //coming to MONTHLY view from WEEKLY view
            {
                var dates = userdate.split("-");
                var date2 = this.getScreenWeekDate(1, dates[1]);        
                this.setMonthDate(date2);
            }
            //analyzedeo();
        },
        
        getDistrict: function() {
            var districtData = this._references.districtdataFeed.getDistrict();
            if (districtData == false) {
                return false;
            }
            this._renderDistrict(districtData);
            this.initSelect2();
        },
        
        getDeo: function() {
            var deoData = this._references.deodataFeed.getDeo();
            if (deoData == false) {
                return false;
            }
            this._renderDeo(deoData);
            this.initSelect2();
        },
        
        analyzeDeo: function(){
            var references = this._references
            var mode;
            var s_list = [];
            var a_list = [];
            var datelist = [];
         
            if ($("#daily").hasClass("active") == true)
            { 
                mode = 1;
                var start_date = this.getScreenDate(2);
                var end_date = this.getScreenDate(3);
             
                s_list.push(0);
                a_list.push(0);
             
                var date_for_datelist = this.getScreenDate(1);

                var date = date_for_datelist.getDate();        
                var mon = references.months[date_for_datelist.getMonth()];
             
                k = date + " "+ mon;
             
                datelist.push(k);   
            }
         
            else if ($("#weekly").hasClass("active") == true) 
            { 
                mode = 2;
                var userdate = jQuery('#dateshow').html(); 
                var dates = userdate.split("-");
                
                var start_date = this.getScreenWeekDate(2, dates[0]);
                var end_date = this.getScreenWeekDate(2, dates[1]);     
             
                var start_date_for_datelist = this.getScreenWeekDate(1, dates[0]);
            
                for (var i = 0; i <= 6; i++) 
                {
                    s_list.push(0);
                    a_list.push(0);
                 
                    var date = start_date_for_datelist.getDate();          
                    var mon = references.months[start_date_for_datelist.getMonth()];
                 
                    var k = date + " "+ mon;
                 
                    datelist.push(k);   
                 
                    start_date_for_datelist.setDate(start_date_for_datelist.getDate() + 1);
                }
            }
            else if ($("#monthly").hasClass("active") == true) 
            { 
                var userdate = jQuery('#dateshow').html();
                var getmon = userdate.split(" ");
                var mon = getmon[0];
             
                mode = 3;
                var start_date = this.getMonthFirstDate(2);
                var end_date = this.getMonthLastDate();

                var lastdate = end_date.split("-")[2];
                     
                for (var i = 1; i <= lastdate; i++) 
                {
                    datelist.push(i);
                    a_list.push(0);
                    s_list.push(0);
                }
            }
            var that = this
            $.ajax(
                 {
                    type:'GET',
                    data:{ 
                    'deo': references.$selectedDeo,
                    'sdate': start_date,
                    'edate': end_date,
                    'mode': mode,
                    },
                    url:window.location.origin + "/analytics/cocouser/api/getthedeo",
                    
                    success: function(data){

                        var sumscreenings = 0;
                        var sumadoptions = 0;
                        if (mode == 1)
                        {
                             for (var key1 in data.screenings)
                             {
                                s_list[0] = data.screenings[key1];
                                sumscreenings += data.screenings[key1];
                             }
                             for (var key2 in data.adoptions)
                             {
                                a_list[0] = data.adoptions[key2];
                                sumadoptions += data.adoptions[key2];
                             }                       
                        }
                        if (mode == 2)
                        {
                             for (var key1 in data.screenings)
                             {
                                 var keydate = key1.split("-")[2];
                                 keydate = keydate.replace(/^0+/, '');
                                 
                                 for (var i = 0; i <= 6; i++)
                                 {
                                     if (datelist[i].split(" ")[0] == keydate)
                                     {
                                         s_list[i] = data.screenings[key1];
                                     }
                                 }                               
                                 sumscreenings += data.screenings[key1];                             
                             }
                             
                             for (var key2 in data.adoptions)
                             {
                                 var keydate = key2.split("-")[2];
                                 keydate = keydate.replace(/^0+/, '');
                                 
                                 for (var i = 0; i <= 6; i++)
                                 {
                                     if (datelist[i].split(" ")[0] == keydate)
                                     {
                                         a_list[i] = data.adoptions[key2];
                                     }
                                 }                               
                                 sumadoptions += data.adoptions[key2];                               
                             }                           
                        }                   
                        if (mode == 3)
                            {
                                 for (var key1 in data.screenings) 
                                 {
                                    var keydate = key1.split("-")[2];
                                    keydate = keydate.replace(/^0+/, '');
                                    s_list[keydate-1] = data.screenings[key1];
                                    sumscreenings += data.screenings[key1];
                                 }
                                 
                                 for (var key2 in data.adoptions) 
                                 {
                                    var keydate = key2.split("-")[2];
                                    keydate = keydate.replace(/^0+/, '');
                                    a_list[keydate-1] = data.adoptions[key2];
                                    sumadoptions += data.adoptions[key2];
                                 }                           
                            }
                         
                        var lin1 = sumscreenings;
                        var lin2 = sumadoptions;
                        var lin3 = data.persons;
                        if (data.slag == "NA")   {var lin4 = data.slag;}
                        else {var lin4 = data.slag + " days";}
                        if (data.alag == "NA")   {var lin5 = data.alag;}
                        else {var lin5 = data.alag + " days";}
                        
                        $("p#screenings").html(lin1);
                        $("p#adoptions").html(lin2);
                        $("p#persons").html(lin3);
                        $("p#s-lag").html(lin4);
                        $("p#a-lag").html(lin5);
                        
                        that.makeChart(datelist,s_list,a_list);
                    },
                    error: function(data){
                           alert("Sorry! There was an error!");
                   }
                 });
        },
        
        makeChart: function(datelist,s_list,a_list)
        {
             var chart1 = new Highcharts.Chart({         
             chart: {
                 renderTo: 'chartcontainer'
              },
               title: {
                    text: 'DEO Performance',
                    x: -20 //center
                },
                xAxis: {
                    categories: datelist
                },
                yAxis: {
                    title: {
                        text: 'Entries made'
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }]
                },

                plotOptions: {
                    series: {
                        cursor: 'pointer',
                        point: {
                            events: {
                                click: function() {
                                    //dateformatted = new Date (yyyy, mm, dd);
                                    if ($("#weekly").hasClass("active") == true)
                                        {
                                            var userdate = document.getElementById('dateshow').innerHTML;
                                            var dates = userdate.split("-");
                                            var date1 = dates[0].split(" ");
                                            var yyyy = date1[2];
         
                                            curdate = this.category;
                                            var dd = curdate.split(' ')[0];
                                            var mon = curdate.split(' ')[1];
                                            var mm = getmonthnofromname(mon);
                                            
                                            if(dd<10) {dd='0'+dd}
                                            if(mm<10) {mm='0'+mm}
                                            
                                            var dateformatted = new Date (yyyy, mm, dd);
                                            
                                            makeactive(1);
                                            setdate(0, dateformatted);
                                            analyzedeo();                                   
                                      }
                                    else if ($("#monthly").hasClass("active") == true)
                                      {
                                        var userdate = document.getElementById('dateshow').innerHTML;
                                        var splitteduserdate = userdate.split(" ");
                                        
                                        var mon = splitteduserdate[0];
                                        var yyyy = splitteduserdate[1];
                                        
                                        var mm = getmonthnofromname(mon);
                                        
                                        if(mm<10) {mm='0'+mm}                           
                                        var dd = this.category;
                                        if(dd<10) {dd='0'+dd}

                                        var dateformatted = new Date (yyyy, mm, dd);                                
                                                                        
                                        makeactive(1);
                                        setdate(0, dateformatted);
                                        analyzedeo();    
                                      }
                                }
                            }
                        }
                    }
                },
                series: [{
                    name: 'Screenings',
                    data: s_list
                }, {
                    name: 'Adoptions',
                    data: a_list
                }]
             });   
        },

        _onDistrictDataProcessed: function() {
            this.getDistrict();
        },
        
        _onDeoDataProcessed: function() {
            this.getDeo();
        },
        
        _onVideoDataProcessed: function() {
            this.getCollectionVideoDropDown();
        },
        
        _onGoBtnClick: function(e) {
            e.preventDefault();
            var references = this._references
            jQuery('#deolist').addClass('nodisplay');      
            jQuery('#thegrid').removeClass('hidden');
            jQuery('#deobox').removeClass('hidden');
            
            var selectedDeos=[];
            references.$deoList.find(":selected").each(function(){
                selectedDeos.push(
                        {
                            deo_id: jQuery(this).val(),
                            deo_name: jQuery(this).text()
                        });
               });
            console.log(selectedDeos);
            this._renderDeoTab(selectedDeos);
            this.analyzeDeo();
        },
        
        _onDayTabClick: function(e) {
            e.preventDefault();
            var references = this._references
            references.$dayTab.addClass('active');
            references.$weekTab.removeClass('active');
            references.$monthTab.removeClass('active');
            
            this.setDay();
            this.analyzeDeo();
            
        },
        
        _onWeekTabClick: function(e) {
            e.preventDefault();
            var references = this._references
            references.$dayTab.removeClass('active');
            references.$weekTab.addClass('active');
            references.$monthTab.removeClass('active');
            this.setWeek()
            this.analyzeDeo();
        },
        
        _onMonthTabClick: function(e) {
            e.preventDefault();
            var references = this._references
            references.$dayTab.removeClass('active');
            references.$weekTab.removeClass('active');
            references.$monthTab.addClass('active');
            this.setMonth()
            this.analyzeDeo();
        },
        
        _onNextPointerClick: function(e) {
            e.preventDefault();
            if ($("#daily").hasClass("active") == true)
            {
                 this.setDate(1, this.getScreenDate(1));    
            }
            else if ($("#weekly").hasClass("active") == true)
            {
                var userdate = jQuery('#dateshow').html(); 
                var dates = userdate.split("-");
                
                var date1 = this.getScreenWeekDate(1, dates[0]);
                var date2 = this.getScreenWeekDate(1, dates[1]);
                
                this.setWeekTwoDates(1, date1, date2);
            }
            else if ($("#monthly").hasClass("active") == true)
            {
                var d = this.getMonthFirstDate(1);
                d.setMonth(d.getMonth() + 1);
                this.setMonthDate(d);        
            }    
            this.analyzeDeo();
        },
        
        _onPrevPointerClick: function(e) {
            e.preventDefault();
            if ($("#daily").hasClass("active") == true)
            {
                 this.setDate(-1, this.getScreenDate(1));       
            }
            else if ($("#weekly").hasClass("active") == true)
            {
                var userdate = jQuery('#dateshow').html(); 
                var dates = userdate.split("-");
                
                var date1 = this.getScreenWeekDate(1, dates[0]);
                var date2 = this.getScreenWeekDate(1, dates[1]);

                this.setWeekTwoDates(-1, date1, date2);
            }    
            else if ($("#monthly").hasClass("active") == true)
            {
                var d = this.getMonthFirstDate(1);     
                d.setMonth(d.getMonth() - 1);
                this.setMonthDate(d);        
            }
            this.analyzeDeo();
        },
        
        _renderDistrict: function(districtData) {
            var references = this._references;
            var renderData = {
                    district: districtData
           };
            var renderedDistrict = viewRenderer.render(districtTemplate, renderData);
            this._references.$districtContainer.html(renderedDistrict);
            
            references.$districtList = jQuery('.js-districtlist');
            
            this._boundFunctions.onDistrictChosen = this._onDistrictChosen.bind(this);
            references.$districtList.on('change', this._boundFunctions.onDistrictChosen);
            
        },
        
        _renderDeo: function(deoData) {
            var references = this._references;
            
            var renderData = {
                    deo: deoData
           };
           var renderedDeo = viewRenderer.render(deoTemplate, renderData);
           this._references.$deoContainer.html(renderedDeo);
            
           references.$deoList = jQuery('.js-deolist');
            
        },
        
        _renderDeoTab: function(deoDataTab) {
            
            var references = this._references;
            
            var renderData = {
                    deo: deoDataTab
           };
           var renderedDeoTab = viewRenderer.render(deoTabTemplate, renderData);
           references.$deoTabContainer.html(renderedDeoTab);
           references.$deoTabContainer.find("li:first a").addClass('active');
           references.$selectedDeo = references.$deoTabContainer.find("li:first a").attr("id");
           var that = this;
           references.$deoTabContainer.find("li").click(function(e) 
           {
               references.$deoTabContainer.find("li").each(function(e)
                       {
                           jQuery(this).find("a").removeClass('active');
                       });
               jQuery(this).find("a").addClass('active');
               references.$selectedDeo = jQuery(this).find("a").attr("id");
               that.analyzeDeo();
           });
           
            
        },
        
        initSelect2: function(){
            var references = this._references;
            try{
                $(".chosen-select").select2({no_results_text: "No results match", width: "100%", placeholder: "Choose Username"});
               }
            catch(err){
                $("select.chosen-select").select2({no_results_text: "No results match", width: "100%", placeholder: "Choose Username"});
            }
            
        },
        
        _onPartnerChosen: function(){
            var references = this._references;
            
            if( references.$partnerList.val()!=""){
                references.districtdataFeed.addInputParam('limit', false, 0);
                references.districtdataFeed.setInputParam('limit', 0, false);
                references.districtdataFeed.addInputParam('partner', false, references.$partnerList.val());
                references.districtdataFeed.setInputParam('partner', references.$partnerList.val(), false);
                this.getDistrict();
            }
            else{
            //TODO: What happens if value becomes default again
            }
        },
        
        _onDistrictChosen: function(){
            var references = this._references;
            
            if( references.$districtList.val()!=""){
                references.deodataFeed.addInputParam('limit', false, 0);
                references.deodataFeed.setInputParam('limit', 0, false);
                references.deodataFeed.addInputParam('partner', false, references.$partnerList.val());
                references.deodataFeed.setInputParam('partner', references.$partnerList.val(), false);
                references.deodataFeed.addInputParam('district', false, references.$districtList.val());
                references.deodataFeed.setInputParam('district', references.$districtList.val(), false);
                this.getDeo();
            }
            else{
            //TODO: What happens if value becomes default again
            }
        },
        
        setInputParam: function(key, value, disableCacheClearing) {
            this._references.dataFeed.setInputParam(key, value, disableCacheClearing);
        },

        _onInputParamChanged: function() {
            this.getCollectionDropDown();
        },
        
        destroy: function() {
            this.base();

            // TODO: clean up
        }
    });

    return DeoAnalyticsViewController;
});
