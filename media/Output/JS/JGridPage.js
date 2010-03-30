// JavaScript Document

// width and height of screen and inner window
var myWidth  = screen.width;
var myHeight = screen.height;

//var winWidth  = window.innerWidth;
//var winHeight = window.innerHeight;

var iewinWidth = document.documentElement.clientWidth;
var iewinHeight = document.documentElement.clientHeight;

// positioning of the expandedview3 div(container for the overlay expanded charts)
var top3  = .05*(iewinHeight);
var left3 = .03*(iewinWidth);

// expanded overlay chart width and height according to the inner window dimensions
var eochartwidth = .95*(.9*(iewinWidth));
var	eochartheight= .85*(.9*(iewinHeight));   


function zoomIn(temp){  		        
		
        var value = temp; 
                
		// fill missing IE properties		
    	if (!window.innerWidth) { 
    		$("div#expandview3").uncorner(); 
    		     	
    	}
    	else{
    		$("div#expandview3").corner();  
    	}
    	
        switch (value)
		{
			case 1:
  				$("div#expandviewtitle").text('Geographical distribution of Videos');
  				$('div#expandview4').html('<div id="alpha1"></div>'); 
				geog_wise_pie1.write("alpha1");
  				break;
			case 2:
  				$("div#expandviewtitle").text('Videos produced per Month');
  				$('div#expandview4').html('<div id="alpha1"></div>'); 
				monthbar1.write("alpha1");
  				break;
  			case 3:
  				$("div#expandviewtitle").text('Videos produced over Time');
  				$('div#expandview4').html('<div id="alpha1"></div>'); 
				videoprod_line1.write("alpha1");
  				break;
  			case 4:  				
  				$("div#expandviewtitle").text('Videos per Practice');
  				$('div#expandview4').html('<div id="alpha1"></div>');
  				practice1.write("alpha1");
  				break;
  			case 5:
  				$("div#expandviewtitle").text('Videos per Language');
  				$('div#expandview4').html('<div id="alpha1"></div>');
  				language1.write("alpha1");
  				break;			
			case 6:
  				$("div#expandviewtitle").text('Videos per Type');
  				$('div#expandview4').html('<div id="alpha1"></div>');
  				type_wise_pie1.write("alpha1");
  				break;			
		}
		
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
        
			
}

function expandviewclose(){ 	     

	$("div#expandviewclosebtn").click( function(){			
        	$("div#expandview3").hide();        	
        	$("div#expandview1").fadeOut();     			
	});	
}
//TODO: Make this as on video page. 
function expandviewoverview(){ 	     

	// fill missing IE properties
    	if (!window.innerWidth) { 
    		$("div#expandview3").uncorner();   		
    		top3 = .03*(iewinHeight);
    		left3 = .03*(iewinWidth);    	
        	//alert(eochartwidth +"yup"+eochartheight);
        	winWidth = iewinWidth; 
    	}
    	else{
    		$("div#expandview3").corner();  
    	}


	$("div#expandviewbtn").click( function(){       
		$("div#expandview1").css({
                    "top": "0px",
                    "left":"0px",
                    "width":myWidth,
                    "height":myHeight,
                    "opacity":"0.7"                      
        });        
        $("div#expandview3").css({
            "top": top3,
            "left":left3,
            "width":.9*(iewinWidth)                                                                                         
    	}); 
    	//alert(.9*(window.innerWidth));        
       	$("div#expandview1").fadeIn();        	   
        $("div#expandview3").show();          			
		$("div#expandviewtitle").text('Cumulative Line Graph');
		$('div#expandview4').append('<div id="flashcontent1"></div>');
  		so1.write("flashcontent1");
	
	});
}

function defaultload(){  		       
                       
            $("div#navmenu").corner();            
            $("div#navmenutitle").corner("7px");
                                    
            //$("div#subgraphdiv1titledesc2").corner("5px");
            $("#searchbody").gradient({ from: 'cff988', to: 'ffffff' });
            $("div#baselinegraph").gradient({ from: 'cff988', to: 'ffffff' });
            
            $("div#analytics").corner("5px");
            
            //$("div#default").corner("round 8px").parent().css('padding', '4px').corner("round 10px")
            //$("div#default").corner("keep");
            $("div#default").corner();  
                    
            $("div#table2td2div").corner("round 4px");          
            
            $("div#graphdiv0title").gradient({ from: 'e1fa9d', to: 'b6ea27' });
            $("div#graphdiv1title").gradient({ from: 'e1fa9d', to: 'b6ea27' });
            //$("div#moduletd0div").corner("round 4px");            
                                    
            
}

function clicktable2tdv2() {            

            $("div#table2tdv2desc").hide(); 
    
            $("div#table2tdv2").mouseover(function(){ 
               	$(this).find("div#table2tdv2desc").removeAttr('disabled');	
                $(this).find("div#table2tdv2desc").show();
                //$("div#table2tdv2").find("div#table2tdv2desc").fadeOut(9000);    
            }); 
           
            $("div#table2tdv2").mouseleave(function(){    
                $(this).find("div#table2tdv2desc").hide();
            });
}
        
function chk(){
    
   // $("div#table2tdv3").text($("img").attr('src','Images/table2tddefaultbg1.png')); 
   
    $("img#sort").bind("click", function() {
        //$("img#sort").attr("src",Pic[2]);
        //if(src =Pic[0] ){ alert("flagdefault"+flagdefault)};
        //if(src =Pic[1] ){alert("flagdefault1"+flagdefault)/*flagascen = 1; /*alert("hi0")*/};
        //if(src =Pic[2] ){alert("flagdefault2"+flagdefault)/*flagdesc = 1; /*alert("hi0")*/};
        var src = ($(this).attr("src") == Pic[1])
                    ? Pic[2] : Pic[1];  
        $(this).attr("src", src);
        
        if(src =Pic[1] ){imgcount = 1};
        if(src =Pic[2] ){imgcount = 2; /*alert("hi0")*/};
        
    });    
        
} // chk() end


function gridview(){ 

    	    
	// for the default view
    $("div#tableheader").find("div#tableheaderleft").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderleft").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(Images/columnbgheader.png)');	            
    });
	
	// for the Overview div
    $("div#tableheader").find("div#tableheaderright").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderright").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(Images/columnbgheader.png)');	            
    });

	
	$("table#table2").find("td#table2td").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#d6fb75');
		   	  $(this).find("div#table2tdv1").fadeIn();			  
    });  
	
    $("table#table2").find("td#table2td").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e1fb9b');
		   	  $(this).find("div#table2tdv1").fadeOut();
		   	  $(this).find("img#sort").attr("src", Pic[0]);	            
    });
    
    $("table#table2").find("td#table2tdf").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#d6fb75');
		   	  $(this).find("div#table2tdv1").fadeIn();			  
    });  
	
    $("table#table2").find("td#table2tdf").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e1fb9b');
		   	  $(this).find("div#table2tdv1").fadeOut();
		   	  $(this).find("img#sort").attr("src", Pic[0]);	            
    });
    
	
	$("table#table2").find("td#table2td1").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e9fbba');			  
    });  
	
    $("table#table2").find("td#table2td1").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#effbcf');	            
    });
    $("table#table2").find("td#table2td4").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e9fbba');			  
    });  
	
    $("table#table2").find("td#table2td4").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#effbcf');	            
    });
    $("table#table2").find("td#table2td5").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e9fbba');			  
    });  
	
    $("table#table2").find("td#table2td5").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#effbcf');	            
    });
	
	// timelinedesc1
	$("div#gridfooter").find("div#timelinedesc1").hide();
	
	$("div#timelinedesc").find("div#timelinedescfooter1").click(function() {
        // alert("hi");
        $("div#gridfooter").find("div#timelinedesc1").removeAttr('disabled');
		$("div#gridfooter").find("div#timelinedesc1").show();
		$(this).hide();
		$("div#timelinedesc").find("div#timelinedescfooter").text('');
		//$("div#gridfooter").find("div#timelinedesc").css('border-bottom', '0px');
    });
    
	$("div#timelinedesc1").find("div#timelinedesc1btntop").click(function() {
        // alert("hi");        
		$("div#gridfooter").find("div#timelinedesc1").hide();
		$("div#gridfooter").find("div#timelinedesc1").attr('disabled','true');
		$("div#timelinedesc").find("div#timelinedescfooter1").fadeIn('slow');
		$("div#timelinedesc").find("div#timelinedescfooter").text('Above are the pre-chosen dates. Customize your own range of timeline');
		//$("div#gridfooter").find("div#timelinedesc").css('border-bottom', '1px');
    });
	
};  

function datepick(){
	
	$("#inlinedatepicker1").calendar({
	    parentElement: '#inlinedatepicker1-container',
	    dateFormat: '%Y-%m-%d'	
	});
	
	// calender for inlinedatepicker2
	$("#inlinedatepicker2").calendar({
	    parentElement: '#inlinedatepicker2-container',
	    dateFormat: '%Y-%m-%d'	
	});
	//$("#inlinedatepicker1").simpleDatepicker({ changeYear: true });
	//$("#inlinedatepicker1").simpleDatepicker({ changeMonth: true });
	
	
	//$("#datepicker1").datepicker({dateFormat: 'dd/mm/yy', minDate: new Date(2006, 10 - 1, 1)});
	//$("#datepicker2").datepicker({dateFormat: 'dd/mm/yy', minDate: new Date(2006, 10 - 1, 1)});
	//$("#datepicker1").datepicker({showButtonPanel: true});
	//$('#inlinedatepicker1').datepicker('option', 'changeYear', true);
	//$('#inlinedatepicker1').datepicker('option', 'changeMonth', true);
	
	
	$("div#timelinedesc").find("input#datepicker1").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e4f1c9');			  
    });  
	
    $("div#timelinedesc").find("input#datepicker1").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e8e8e7');	            
    });
	
	$("div#timelinedesc").find("input#datepicker2").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e4f1c9');			  
    });  
	
    $("div#timelinedesc").find("input#datepicker2").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e8e8e7');	            
    });	
	
};

function timelinedesc1close(){

 $("div#timelinedesc1").hide();
 $("div#timelinedesc").find("div#timelinedescfooter1").fadeIn('slow');
 $("div#timelinedesc").find("div#timelinedescfooter").text('Above are the pre-chosen dates. Customize your own range of timeline');   
};

function dateRange() {
	alert("Hi");	

};
/** This is run when the page is fully loaded */
$(document).ready(function(){		
	$("div#gridfooter").find("div#timelinedesc1").hide();   
    gridview();
	datepick();
	chk();	
	expandviewoverview();
	expandviewclose();
	timelinedesc1close();
	clicktable2tdv2();
	defaultload();	
	//sortval();
});
	