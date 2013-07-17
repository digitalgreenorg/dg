// JavaScript Document

// help bubbles for column headers
function clicktable2tdv2() {            

            $("div#table2tdv2desc").hide(); 
    
            $("div#table2tdv2").mouseover(function(){                	
                $(this).find("div#table2tdv2desc").show();
                //$("div#table2tdv2").find("div#table2tdv2desc").fadeOut(9000);    
            }); 
           
            $("div#table2tdv2").mouseleave(function(){    
                $(this).find("div#table2tdv2desc").hide();
            });
}


// changing background of the column headers on mouseovers in the overview page  

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
	
};

/** This is run when the page is fully loaded */
$(document).ready(function(){		
	$("div#gridfooter").find("div#timelinedesc1").hide();   
    gridview();	
	clicktable2tdv2();		
});
	