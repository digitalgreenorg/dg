
// width and height of screen and inner window
var myWidth  = screen.width;
var myHeight = screen.height;

var iewinWidth = document.documentElement.clientWidth;
var iewinHeight = document.documentElement.clientHeight;

// positioning of the expandedview3 div(container for the expanded charts)
var top3  = .05*(iewinHeight);
var left3 = .03*(iewinWidth);

// expanded overlay chart width and height according to the inner window dimensions
var eochartwidth = .95*(.9*(iewinWidth));
var	eochartheight= .85*(.9*(iewinHeight));

// function called when clicked on the zoominbutton link of the video module
function zoomIn(temp1, temp2)
{ 		
		var header    = temp2;             
                
        $("div#expandview1").css({
                    "top": "0px",
                    "left":"0px",
                    "width":myWidth,
                    "height":myHeight,
                    "opacity":"0.7",                                                              
        });
        
        $("div#expandview3").css({
                    "top": top3,
                    "left":left3,
                    "width":0.9*(iewinWidth)                                                                                 
        });          
       	$("div#expandview1").fadeIn();        	   
        $("div#expandview3").show();       
     
        
        $("div#expandviewtitle").text(header);
  		$("div#expandview4").html('<div id="alpha1"></div>');
		temp1.write('alpha1');
}


function expandviewclose(){ 	     

	$("div#expandviewclosebtn").click( function(){			
        	$("div#expandview3").hide();        	
        	$("div#expandview1").fadeOut();     			
	});	
}

/* This is run when the page is fully loaded */
$(document).ready(function(){		
	expandviewclose();	
});