// JavaScript Document
 
var selecteddeoname;
 
var pflag = 0;
var diflag = 0;
var deflag = 0;
var chosendeos = [];
    
function partnersetter()
    {  	
    	if (pflag == 0)
    	{
        	document.getElementById('partnerlist').classList.remove('nodisplay');
        	document.getElementById('partnerlist').classList.add('blockdisplay');
        	pflag = 1;            		
    	}
    	else if (pflag == 1)
		{
        	document.getElementById('partnerlist').classList.remove('blockdisplay');
        	document.getElementById('partnerlist').classList.add('nodisplay');
        	pflag = 0;            		
    	}  
    	
        $.ajax(
        {
         type:'GET',
         url: window.location.origin + "/analytics/cocouser/api/getpartner",
        
         success: function(data){
             var listitems = '';
             for (var j = 0; j < data.length; j++) 
             {                         
               listitems += '<li class=' + '"item h-overflow"' + 'id="' + data[j].id+  '"onclick="' + 'setpartnerlistdiv(this)' + '">' + data[j].partner_name + '</li>';
             }
             $("ul#partnerlist").html(listitems);
         },
         error: function(data){
             alert("Sorry there was an error!");
        }
        });
    }

function setpartnerlistdiv(text)
    {   
 	    var partner_id = text.id;
 	    var partner_name = text.innerText.trim();
    	$("div#partnername").html(partner_name); 
    	document.getElementById('districtlist').classList.remove('nodisplay');
    	document.getElementById('districtlist').classList.add('blockdisplay');
    	diflag = 1;
    	districtfilter(partner_id);
    }

function districtsetter()
    {
    	if (diflag == 0)
    	{
        	document.getElementById('districtlist').classList.remove('nodisplay');
        	document.getElementById('districtlist').classList.add('blockdisplay');
        	diflag = 1;
    	}
    	else if (diflag == 1)
		{
        	document.getElementById('districtlist').classList.remove('blockdisplay');
        	document.getElementById('districtlist').classList.add('nodisplay');
        	diflag = 0;
    	}     	
    }
    
function districtfilter(partner_id)
    {           
       $.ajax(
       {
        type:'GET',
        data:{ 
        'partner': partner_id,
        },
        url: window.location.origin + "/analytics/cocouser/api/getdistrict",
        
        success: function(data){

            var listitems = '';
            for (var i = 0; i < data.length; i++) 
            {
           	 
              listitems += '<li class=' + '"item h-overflow"' + 'id="' + data[i]+  '"onclick="' + 'setdistrictlistdiv(this' + ',' + partner_id + ')' + '">' + data[i] + '</li>';
            }
            $("ul#districtlist").html(listitems);
        },
        error: function(data){
                alert("Sorry there was an error!");
        }
      });
    }
    
function setdistrictlistdiv(text, partner_id)
    {	
    	chosendeos = [];    	
 	    var district_name = text.innerText.trim();
    	$("div#districtname").html(district_name);   
    	deofilter(district_name, partner_id);
    	document.getElementById('deolist').classList.remove('nodisplay');
    	document.getElementById('deolist').classList.add('blockdisplay');
    	deflag = 1;    	
    }    

function deofilter(district_name, partner_id)
    {       
       $.ajax(
       {
          type:'GET',
          data:{ 
          'partner': partner_id,
          'district': district_name,
          },
          url: window.location.origin + "/analytics/cocouser/api/getdeo",
          
          success: function(data){

              var listitems = '';
              for (var i = 0; i < data.length; i++) 
              {
             	 listitems += '<li id="' + i + data[i].deo_id + '"class=' + '"item h-overflow deonotselected hdg-trunc"' + 'onclick="' 
             	 + "makedeochecked('" + i + data[i].deo_id + "','" + data[i].deo_id + "','" + data[i].deo_name + "')" + '">' + 
             	 '<input id ="' + data[i].deo_id + '"type=' + '"checkbox"' + '/>' + data[i].deo_name + '</li>';
              }
              $("ul#deolist").html(listitems);
          },
          error: function(data){
                 alert("Sorry there was an error!");
         }
       });
    }
    
function makedeochecked(itemid, deoid, deo_name)
    {
    	if ($('#' + itemid).hasClass("deonotselected"))
    		{
    			$('#' + itemid).removeClass("deonotselected");
    			$('#' + itemid).addClass("deoselected");
    			$('#' + deoid).prop('checked', true);
    			chosendeos.push(deo_name);	
    		}
    	else if ($('#' + itemid).hasClass("deoselected"))
    		{
    			$('#' + itemid).removeClass("deoselected");
    			$('#' + itemid).addClass("deonotselected");
    			$('#' + deoid).prop('checked', false);
    			var index = chosendeos.indexOf(deo_name);
	 	    	chosendeos.splice(index,1);
    		}
    }
    
function deosetter()
    {
    	if (deflag == 0)
    	{
        	document.getElementById('deolist').classList.remove('nodisplay');
        	document.getElementById('deolist').classList.add('blockdisplay');
        	deflag = 1;
    	}
    	else if (deflag == 1)
		{
        	document.getElementById('deolist').classList.remove('blockdisplay');
        	document.getElementById('deolist').classList.add('nodisplay');
        	deflag = 0;
    	}     	
    }
    
function onbodyload()
   {
	  var today = new Date();
	  setdate(0, today);
	  setweekfromsingledate(new Date());
   }

function settheday()
   {
	   var userdate = document.getElementById('dateshow').innerHTML;
	   var first = userdate.split(" ");

	   if (first[0] == parseInt(first[0])) //coming to DAILY view from WEEKLY view
	   {
		   dates = userdate.split("-");
		   date1 = getdateonscreenforweek(1, dates[0]);		   
		   setdate(0, date1);
	   }
	   else if (first[0] == "Jan" || first[0] == "Feb" || first[0] == "Mar" || first[0] == "Apr" || first[0] == "May" || 
			   first[0] == "Jun" || first[0] == "Jul" || first[0] == "Aug" || first[0] == "Sep" || first[0] == "Oct" || 
			   first[0] == "Nov" || first[0] == "Dec") 
		   //coming to DAILY from MONTHLY			   
	   {
		   d = getfirstdateofselectedmonth(1);
		   
		   var day = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
		   var dayofweek = day[d.getDay()];
		   var month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
		   var mon = month[d.getMonth()];
		   
		   d = dayofweek+' '+ d.getDate() +' '+mon+' '+d.getFullYear();
		   $("div#dateshow").html(d);		   
	   }
	   analyzedeo();
   }
  
function settheweek()
 	{
 	   var userdate = document.getElementById('dateshow').innerHTML;
	   var first = userdate.split(" ");
	   
	   if (first[0] == "Sun" || first[0] == "Mon" || first[0] == "Tue" || first[0] == "Wed" || first[0] == "Thu"
		   || first[0] == "Fri" || first[0] == "Sat") //coming to WEEKLY view from DAILY view	   
	   {
			var mydate = getdateonscreen(1);	
			setweekfromsingledate(mydate);
	   }
	   else if (first[0] == "Jan" || first[0] == "Feb" || first[0] == "Mar" || first[0] == "Apr" || first[0] == "May" || 
			   first[0] == "Jun" || first[0] == "Jul" || first[0] == "Aug" || first[0] == "Sep" || first[0] == "Oct" || 
			   first[0] == "Nov" || first[0] == "Dec") //coming to WEEKLY from MONTHLY view
	   {
		   d = getfirstdateofselectedmonth(1);	   
		   setweekfromsingledate(d);
	   }
	   analyzedeo();
 	}
	
function setthemonth()
	{
	   var userdate = document.getElementById('dateshow').innerHTML;
	   var first = userdate.split(" ");

	   if (first[0] == "Sun" || first[0] == "Mon" || first[0] == "Tue" || first[0] == "Wed" || first[0] == "Thu"
		   || first[0] == "Fri" || first[0] == "Sat") //coming to MONTHLY view from DAILY view
	   {
			var mydate = getdateonscreen(1);
			setmonthfromdate(mydate);
	   }
	   else if (first[0] == parseInt(first[0])) //coming to MONTHLY view from WEEKLY view
	   {
		   dates = userdate.split("-");
		   date2 = getdateonscreenforweek(1, dates[1]);		   
		   setmonthfromdate(date2);
	   }
	   analyzedeo();
	}
	
function getfirstdateofselectedmonth(cn)
	{
	   var data = document.getElementById('dateshow').innerHTML;
	   var usermonth = data.split(" ");
	   
	   d = new Date (usermonth[1], getmonthnofromname(usermonth[0]), '01');
	   
       if (cn == 2)
		 {    	   
    	   mm = d.getMonth() + 1;
		   d = d.getFullYear()+'-'+mm+'-'+d.getDate();
		 }   
	   return d;
	}
	
function getlastdateofselectedmonth()
	{
		var d = getfirstdateofselectedmonth(1);
		
		var ld = new Date(d.getFullYear(), d.getMonth()+1, 0);
		
		ldmm = ld.getMonth() + 1;
		ld = ld.getFullYear()+'-'+ldmm+'-'+ld.getDate();
		
		return ld;
		
	}

function setmonthfromdate(d)
	{
		var month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
		var mon = month[d.getMonth()];
		
		var yyyy = d.getFullYear();

   	    d = mon +' '+ yyyy;
		$("div#dateshow").html(d);
	}
	
function setdate(counter, d)
 	{
 	   if (counter == -1)  {d.setDate(d.getDate() - 1);}
 	   else if (counter == 1)  {d.setDate(d.getDate() + 1);}
 	   
	   var dd = d.getDate();
	   
	   var day = ['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
	   var month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

	   var day = day[d.getDay()];
	   var mon = month[d.getMonth()];

	   var yyyy = d.getFullYear();

	   if(dd<10) {dd='0'+dd} 

	   d = day+' '+ dd+' '+mon+' '+yyyy;
	   $("div#dateshow").html(d);
 	}
 
function getdateonscreen(cn)
 	{
 	   var userdate = document.getElementById('dateshow').innerHTML; 
	   datesplitted = userdate.split(" ");

	   var dd = datesplitted[1];
	   
	   var yyyy = datesplitted[3];
	   var mm = getmonthnofromname(datesplitted[2]);
   
	   if (cn == 2) {mm = mm+1}
	   if(mm<10) {mm='0'+mm}
   
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
 	}
 	
function setweekfromsingledate(d)
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
 	  
	  setweekfromtwodates(0, startweek, endweek)
 	}

function setweekfromtwodates(counter, startweek, endweek)
 	{
 		
  	  if (counter == -1)  {startweek.setDate(startweek.getDate() - 7); endweek.setDate(endweek.getDate() - 7);}
 	  else if (counter == 1)  {startweek.setDate(startweek.getDate() + 7); endweek.setDate(endweek.getDate() + 7);}
  	   
 	  var month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
 	  var startweekmon = month[startweek.getMonth()];
 	  var endweekmon = month[endweek.getMonth()];
 	 
	  var yrstartweek = startweek.getFullYear();
	  var yrendweek = endweek.getFullYear();

	  d = startweek.getDate()+ ' ' + startweekmon + ' ' + yrstartweek + '-'+ endweek.getDate() +' '+ endweekmon + ' '+ yrstartweek;  

	  $("div#dateshow").html(d);	
 	}
 	
function getdateonscreenforweek(cn, rdate)
 	{
	   date = rdate.split(" ");
	   
	   var dd = date[0];	   
	   var yyyy = date[2];
	   var mm = getmonthnofromname(date[1]);
	   if (cn == 2) {mm = mm+1}
	   if(mm<10) {mm='0'+mm}
   
	   if (cn==1)
		 {
		   dateformatted = new Date (yyyy, mm, dd);		   
		 }
	   else if (cn == 2)
		 {
		   dateformatted = yyyy+'-'+mm+'-'+dd;
		 }	
	   return dateformatted;
 	}
 	
function getmonthnofromname(mon)
 	{
 	   if (mon == "Jan") {mm = 0;}
	   else if (mon == "Feb") {mm = 1;}
	   else if (mon == "Mar") {mm = 2;}
	   else if (mon == "Apr") {mm = 3;}
	   else if (mon == "May") {mm = 4;}
	   else if (mon == "Jun") {mm = 5;}
	   else if (mon == "Jul") {mm = 6;}
	   else if (mon == "Aug") {mm = 7;}
	   else if (mon == "Sep") {mm = 8;}
	   else if (mon == "Oct") {mm = 9;}
	   else if (mon == "Nov") {mm = 10;}
	   else if (mon == "Dec") {mm = 11;}
 
	   return mm;
 	}
 	
function movenext()
   {

	   if ($("#daily").hasClass("active") == true)
	   {
			setdate(1, getdateonscreen(1));	   
	   }
	   else if ($("#weekly").hasClass("active") == true)
	   {
	  	   var userdate = document.getElementById('dateshow').innerHTML; 
		   dates = userdate.split("-");
		   
		   date1 = getdateonscreenforweek(1, dates[0]);
		   date2 = getdateonscreenforweek(1, dates[1]);
		   
		   setweekfromtwodates(1, date1, date2);
	   }
	   else if ($("#monthly").hasClass("active") == true)
	   {
		   var d = getfirstdateofselectedmonth(1);
		   d.setMonth(d.getMonth() + 1);
		   setmonthfromdate(d);		   
	   }	
	   analyzedeo();
   }

function moveprev()
   {
	   if ($("#daily").hasClass("active") == true)
	   {
			setdate(-1, getdateonscreen(1));	   
	   }
	   else if ($("#weekly").hasClass("active") == true)
	   {
	  	   var userdate = document.getElementById('dateshow').innerHTML; 
		   dates = userdate.split("-");
		   
		   date1 = getdateonscreenforweek(1, dates[0]);
		   date2 = getdateonscreenforweek(1, dates[1]);

		   setweekfromtwodates(-1, date1, date2);
	   }	
	   else if ($("#monthly").hasClass("active") == true)
	   {
		   var d = getfirstdateofselectedmonth(1);	   
		   d.setMonth(d.getMonth() - 1);
		   setmonthfromdate(d);		   
	   }
	   analyzedeo();
   }
 
function goclicked()
   {	   
	   document.getElementById('deolist').classList.add('nodisplay');      
       document.getElementById("thegrid").classList.remove('hidden');
       document.getElementById("deobox").classList.remove('hidden');
       
       var list = '';
       for (var j = 0; j < chosendeos.length; j++) 
       {
           htmlline = '<li><a id="' + 'deo' + j + '"'+ 'href="' + '#"' + 'class=' + '"js-most-filter"' + 'onclick="' 
           + 'makedeoactive(this'+ ',' + chosendeos.length + ',' + j + ');">' 
           + '<span><span class="' + 'icon"' + '></span>' + chosendeos[j]+ '</span></a></li>';
       	   list += htmlline;
       }
       $("ul#deobox").html(list);
       document.getElementById("deo0").classList.add('active');
       
       deoname = document.getElementById("deo0").innerText.trim();
      
       selecteddeoname = deoname;
              
       analyzedeo();
   }

function makedeoactive(deoname_element, total, val)
   {
	   deoname = deoname_element.innerText.trim();
	   	
	   selecteddeoname = deoname;
	   
       for (var j = 0; j < total; j++) 
       {	  
    	   if (j == val)
    	   {
    		   document.getElementById("deo"+j).classList.add('active');   		   
    	   }
    	   else
    	  {
    		   document.getElementById("deo"+j).classList.remove('active');    		   
    	  }   
       }
       analyzedeo()
   }
   
function analyzedeo()
   {	     
   	var mode;
   	var s_list = [];
   	var a_list = [];
   	var datelist = [];
   	var month = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
   	
   	if ($("#daily").hasClass("active") == true)
    { 
   		mode = 1;
   	   	start_date = getdateonscreen(2);
   	 	end_date = getdateonscreen(3);
   	 	
   	    s_list.push(0);
   	 	a_list.push(0);
   	    
   	 	date_for_datelist = getdateonscreen(1);

		date = date_for_datelist.getDate();		   
		mon = month[date_for_datelist.getMonth()];
		
		k = date + " "+ mon;
		
		datelist.push(k);	
    }
   	
   	else if ($("#weekly").hasClass("active") == true) 
   	{ 
   		mode = 2;
	  	var userdate = document.getElementById('dateshow').innerHTML; 
		dates = userdate.split("-");
		   
		start_date = getdateonscreenforweek(2, dates[0]);
		end_date = getdateonscreenforweek(2, dates[1]);		
		
		start_date_for_datelist = getdateonscreenforweek(1, dates[0]);
	   
		for (var i = 0; i <= 6; i++) 
		{
			s_list.push(0);
			a_list.push(0);
			
			date = start_date_for_datelist.getDate();		   
			mon = month[start_date_for_datelist.getMonth()];
			
			k = date + " "+ mon;
			
			datelist.push(k);	
			
			start_date_for_datelist.setDate(start_date_for_datelist.getDate() + 1);
		}
   	}
   	else if ($("#monthly").hasClass("active") == true) 
   	{ 
   		mode = 3;
   		start_date = getfirstdateofselectedmonth(2);
   		end_date = getlastdateofselectedmonth();

   		lastdate = end_date.split("-")[2];
   				
		for (var i = 1; i <= lastdate; i++) 
		{
			datelist.push(i);
			a_list.push(0);
			s_list.push(0);
		}
   	}
  	
    $.ajax(
            {
               type:'GET',
               data:{ 
               'deo': selecteddeoname,
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
		 				    keydate = key1.split("-")[2];
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
		 				    keydate = key2.split("-")[2];
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
		 					   keydate = key1.split("-")[2];
		 					   keydate = keydate.replace(/^0+/, '');
		 					   s_list[keydate-1] = data.screenings[key1];
		 					   sumscreenings += data.screenings[key1];
		 					}
		   					
		   					for (var key2 in data.adoptions) 
		   					{
		 					   keydate = key2.split("-")[2];
		 					   keydate = keydate.replace(/^0+/, '');
		 					   a_list[keydate-1] = data.adoptions[key2];
		 					   sumadoptions += data.adoptions[key2];
		 					} 		   					
            		   }
					
            	   lin1 = "No. of screenings entered: " + sumscreenings;
            	   lin2 = "No. of adoptions entered : " + sumadoptions;
            	   lin3 = "No. of persons entered   : " + data.persons;
            	   if (data.slag == "NA")	{lin4 = "Average Screening Lag    : " + data.slag;}
            	   else	{lin4 = "Average Screening Lag    : " + data.slag + " days";}
            	   if (data.alag == "NA")	{lin5 = "Average Adoption Lag     : " + data.alag;}
            	   else	{lin5 = "Average Adoption Lag     : " + data.alag + " days";}
            	   
             	   $("p#screenings").html(lin1);
            	   $("p#adoptions").html(lin2);
            	   $("p#persons").html(lin3);
            	   $("p#s-lag").html(lin4);
            	   $("p#a-lag").html(lin5);
            	   
            	   makechart(datelist,s_list,a_list);
               },
               error: function(data){
                      alert("Sorry! There was an error!");
              }
            });
   }
   
function makechart(datelist,s_list,a_list)
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
                        	   
                        	   var userdate = document.getElementById('dateshow').innerHTML;
                    		   var dates = userdate.split("-");
                    		   var date1 = dates[0].split(" ");
                    		   var yyyy = date1[2];

                        	   curdate = this.category;
                        	   console.log(curdate);
                        	   var dd = curdate.split(' ')[0];
                        	   var mon = curdate.split(' ')[1];
                        	   var mm = getmonthnofromname(mon);
                        	   
                        	   if(dd<10) {dd='0'+dd}
                        	   if(mm<10) {mm='0'+mm}
                        	   
                        	   var dateformatted = new Date (yyyy, mm, dd);
                        	   
                        	   console.log(dateformatted);
                        	   
                        	   makeactive(1);
                        	   setdate(0, dateformatted);
                        	   analyzedeo();
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
   }
   
function makeactive(num)
   {
	   if (num==1)
	   {
		   document.getElementById('daily').classList.add('active');
		   document.getElementById('weekly').classList.remove('active');
		   document.getElementById('monthly').classList.remove('active');
	   }
	   else if (num==2)
	   {
		   document.getElementById('weekly').classList.add('active');
		   document.getElementById('daily').classList.remove('active');
		   document.getElementById('monthly').classList.remove('active');
	   }
	   else if (num==3)
	   {
		   document.getElementById('monthly').classList.add('active');
		   document.getElementById('weekly').classList.remove('active');
		   document.getElementById('daily').classList.remove('active');
	   }	   
   }