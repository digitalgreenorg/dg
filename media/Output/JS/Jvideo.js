
// The values of the video details
var languagename,villagename,distname,statename,prodtime,prodenddate,practiceshown,videosummary;

// Displaying the data in the Video Page in Tab wise

var videodesc2 ="<div id='videodatadiv2divdesctop'></div>";
var videodesc41 ="<div id='videodatadiv2divdesctop'></div><table id='videoinfotable' cellspacing='0px' cellpadding='0'><tr><td class='videoinfotd1'> Video Language: ";
var videodesc42 ="</td><td class='videoinfotd2'>Village: ";
var videodesc43 ="</td></tr><tr><td class='videoinfotd1'> District: ";
var videodesc44 ="</td><td class='videoinfotd2'> State: ";
var videodesc45 ="</td></tr><tr><td class='videoinfotd1'> Production Duration: ";
var videodesc46 ="</td><td class='videoinfotd2'> Produced On: "
var videodesc47 ="</td></tr></table>";


function displaynumstat(numstat1,numstat2,numstat3,numstat4,numstat5,numstat6, numstat7,numstat8)
{
	languagename = numstat1;
	villagename = numstat2;
	distname = numstat3;	
	statename = numstat4;
	prodtime = numstat5;
	prodenddate = numstat6;
	practiceshown = numstat7;
	videosummary = numstat8;
	
}

function displaydesc(temp){			
			
			// Adding the background colour to the selected tab            
			
			if(temp==1){			
				$("div#videodatadiv2divdesc").html(videodesc41 + languagename + videodesc42 + villagename + videodesc43 + distname + videodesc44 + statename + videodesc45 + prodtime + videodesc46 + prodenddate + videodesc47);
				$("div#videodatadiv2divdesctop").css('margin-left','0px');					
				//$("table#videoinfotable").slideDown();				
			} //ifends
			
			if(temp==2){			
				$("div#videodatadiv2divdesc").html(videodesc2 + practiceshown);				
				$("div#videodatadiv2divdesctop").css('margin-left','250px');				
			} //ifends
			
			if(temp==3){			
				$("div#videodatadiv2divdesc").html(videodesc2 + videosummary);
				$("div#videodatadiv2divdesctop").css('margin-left','490px');				
			} //ifends
						
}

function defaultload(){ 
					
// Videos Page Help divs			
			
					
			$("div#videodatadiv1div").mouseover(function() {            	
            	$(this).find("div#videodatadiv1help").show();
            });      
            
            $("div#videodatadiv1div").mouseleave(function() {            	
            	$(this).find("div#videodatadiv1help").hide();
            });     
            
            $("td#videodatadiv2td").mouseover(function() { 
            	$(this).css('background-color','#f6f6f6');
            });
            
            $("td#videodatadiv2td").mouseleave(function() {
            	$(this).css('background-color','#ebebeb');
            });
            
            // change the background color for every column of the data stat numbers 
            $("td#videodatadiv1td").mouseover(function() { 
            	$(this).css('background-color','#f6f6f6');
            	$(this).css('border-color','Gray');
            });
            
            $("td#videodatadiv1td").mouseleave(function() {
            	$(this).css('background-color','#ffffff');
            	$(this).css('border-color','#E2E2E2');
            });          
    
            $("table#videodatadiv2").mouseover(function() { 
            	$(this).css('border-color','Gray');
            });
            
            $("table#videodatadiv2").mouseleave(function() {
            	$(this).css('border-color','#e2e2e2');
            });
            
            $("table#videodatadiv3").mouseover(function() { 
            	$(this).css('border-color','Gray');
            });
            
            $("table#videodatadiv3").mouseleave(function() {
            	$(this).css('border-color','#e2e2e2');
            });
            
            // highlighting the right side suggestions column on mouseover
             
            $("td#contentdivrighttd").mouseover(function() { 
            	$(this).css('background-color','#efefef');
            });
            
            $("td#contentdivrighttd").mouseleave(function() {
            	$(this).css('background-color','White');
            });
			
			// Initializing the Date Pick Calender
			$("div#datepickcalender1").calendar({	       		
	       		dateFormat:"%Y-%m-%d",	       		
			});
			
			$("div#datepickcalender2").calendar({	       		
	       		dateFormat:"%Y-%m-%d",	       		
			});
			
			//showing the advanced search option in the Video Search Page
			$("td#advancedsearchopenbtn").click(function() { 
            	$("div.advancedsearchdiv").slideDown();
            	$(this).hide();
            	$("td#advancedsearchclosebtn").show();
            });
            
            
            $("td#advancedsearchclosebtn").click(function() { 
            	$("div.advancedsearchdiv").slideUp();
            	$(this).hide();
            	$("td#advancedsearchopenbtn").show();
            }); 
           
           
           // Paging in the SearchVideo Result page 
            
            $("li#pagingdivli").mouseover(function() { 
            	$(this).css('border-color','#3F3E3E');
            });
            
            $("li#pagingdivli").mouseleave(function() {
            	$(this).css('border-color','Gray');
            });
			


} // function defaultload
//Function to enable/disable and fill option in Selects for region select drop downs
function dochange(src, val) {
    $.ajax({ type: "GET", 
            url: "/analytics/drop_down_val?geog="+src+"&id="+val,
            success: function(html) {                    
            var flag = false;
            $(".geog").each(function() {
                if(flag == true)
                    $(this).val(-1).attr('disabled','disabled');
                if (this.name == src)
                    flag = true;                    
            });
            
           $("#"+src+"Id").html(html).removeAttr('disabled');                   
      }
 });
}

function go(page) {
    var url = new Array();
    var query = $("#searchinput").val();
    if(query!="" && page!=null) {
        window.location.href = '?query='+query+'&page='+page;
        return ;
    }   
    
    if($("#videosuitable").val()!='-1')  url.push("videosuitable="+$("#videosuitable").val());
    if($("#uploads").val()!='-1') url.push("videouploaded="+$("#uploads").val());
    
    partners = $("#partners").val();
    for(i=0;i<partners.length;i++) {
        if(partners[i] !='-1')
            url.push("partner="+partners[i]);
    }
    
    var geog = null, id = '1';
    $(".geog").each(function() {
        if($(this).val()=='-1')
            return false;
        geog = $(this).attr('name');
        id = $(this).val();
    });
    if(geog != null) {
	    url.push("geog="+geog);
	    url.push("id="+id);
    }
    
    if($("#lang").val()!='-1')  url.push("lang="+$("#lang").val());
    season = $("#season").val();
    for(i=0;i<season.length;i++) {
        if(season[i] != '-1')
            url.push("season="+season[i]);
    }
    
    practice = $("#practice").val();
    for(i=0;i<practice.length;i++) {
        if(practice[i] != '-1')
            url.push("prac="+practice[i]);
    }
    if($("#datepickcalender1").html()!="") url.push("from_date="+$("#datepickcalender1").html());
    if($("#datepickcalender2").html()!="") url.push("to_date="+$("#datepickcalender2").html());
    if(page != null) url.push("page="+page);
    
    if(url.length>0) 
        window.location.href = '?'+url.join('&');
}

/* This is run when the page is fully loaded */
$(document).ready(function(){	   
	defaultload();	
	init_box_params();
});