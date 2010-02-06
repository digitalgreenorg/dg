// JavaScript Document

function gridview(){   
	    
	// for the default view
    $("div#tableheader").find("div#tableheaderleft").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderleft").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/columnbgheader.png)');	            
    });
	
	// for the Overview div
    $("div#tableheader").find("div#tableheaderright").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderright").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/columnbgheader.png)');	            
    });
	
	$("table#table1").find("td#table1td2").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/tdbg2.png)');			  
    });  
	
    $("table#table1").find("td#table1td2").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/tdbg1.png)');	            
    });
	
	$("table#table1").find("td#table1td3").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/tdbg2.png)');			  
    });  
	
    $("table#table1").find("td#table1td3").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/tdbg1.png)');	            
    });
	
	$("table#table2").find("td#table2td").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#757575');			  
    });  
	
    $("table#table2").find("td#table2td").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#616161');	            
    });
	
	$("table#table2").find("td#table2td1").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#b0e73a');			  
    });  
	
    $("table#table2").find("td#table2td1").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#d5fe7c');	            
    });
	
	$("div#timelinedesc").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/timelinebg1.png)');			  
    });  
	
    $("div#timelinedesc").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-image', 'url(/media/Output/Images/timelinebg.png)');	            
    });
    
};     


function datepicker(){
	$("#datepicker1").datepicker({dateFormat: 'dd/mm/yy', minDate: new Date(2009, 10 - 1, 1)});
	$("#datepicker2").datepicker({dateFormat: 'dd/mm/yy', minDate: new Date(2009, 10 - 1, 1)});
	
	$("div#timelinedesc").find("input#datepicker1").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#d8fd88');			  
    });  
	
    $("div#timelinedesc").find("input#datepicker1").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e8e8e7');	            
    });
	
	$("div#timelinedesc").find("input#datepicker2").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#d8fd88');			  
    });  
	
    $("div#timelinedesc").find("input#datepicker2").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e8e8e7');	            
    });	
	
};

function dateRange() {
	alert("Hi");	

};
/** This is run when the page is fully loaded */
$(document).ready(function(){   
    gridview();
	datepicker();
	
});
	