
// Displaying the data in the Video Page in Tab wise 

var videodesc1 ="<div id='videodatadiv2divdesctop'></div><table class='he'><tr><td>ge</td></tr></table>";
var videodesc2 ="<div id='videodatadiv2divdesctop'></div>2.dvoifvnfeibnefoibndpfibnepfbnepibnepb";
var videodesc3 ="<div id='videodatadiv2divdesctop'></div>3.oscnvfpvlfbmlkfbmnbnpibneoibnefoib";
var videodesc4 ="<div id='videodatadiv2divdesctop'></div><table id='videoinfotable' cellspacing='0px' cellpadding='0'><tr><td class='videoinfotd1'> Video Language:</td><td class='videoinfotd2'></td></tr><tr><td class='videoinfotd1'> Village:</td><td class='videoinfotd2'></td></tr><tr><td class='videoinfotd1'> District:</td><td class='videoinfotd2'></td></tr><tr><td class='videoinfotd1'> State:</td><td class='videoinfotd2'></td></tr><tr><td class='videoinfotd1'> Video production Start Date:</td><td class='videoinfotd2'></td></tr><tr><td class='videoinfotd1'> Video production End Date:</td><td class='videoinfotd2'></td></tr></table>";

function displaydesc(temp){
			
			
			// Adding the background colour to the selected tab            
			
			if(temp==1){			
				$("div#videodatadiv2divdesc").html(videodesc4);
				$("div#videodatadiv2divdesctop").css('margin-left','5px');					
				//$("table#videoinfotable").slideDown();				
			} //ifends
			
			if(temp==2){			
				$("div#videodatadiv2divdesc").html(videodesc2);				
				$("div#videodatadiv2divdesctop").css('margin-left','250px');				
			} //ifends
			
			if(temp==3){			
				$("div#videodatadiv2divdesc").html(videodesc3);
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


} // function defaultload

/* This is run when the page is fully loaded */
$(document).ready(function(){	   
	defaultload();	
});