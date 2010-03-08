// JavaScript Document

function gridview(){   
	    
	// for the default view
    $("div#tableheader").find("div#tableheaderleft").mouseover(function() {
          // alert("hi1");
		   	  $(this).css('background-image', 'url(Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderleft").mouseleave(function() {
           //alert("hi2");
		   	  $(this).css('background-image', 'url(Images/columnbgheader.png)');	            
    });
	
	// for the Overview div
    $("div#tableheader").find("div#tableheaderright").mouseover(function() {
         //  alert("hi3");
		   	  $(this).css('background-image', 'url(Images/columnbgheader1.png)');			  
    });  
	
    $("div#tableheader").find("div#tableheaderright").mouseleave(function() {
          // alert("hi4");
		   	  $(this).css('background-image', 'url(Images/columnbgheader.png)');	            
    });

	
	$("table#table2").find("td#table2td").mouseover(function() {
         // alert("hi5");
		   	  $(this).css('background-color', '#d6fb75');			  
    });  
	
    $("table#table2").find("td#table2td").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#e1fb9b');	            
    });
	
	$("table#table2").find("td#table2td1").mouseover(function() {
           //alert("hi");
		   	  $(this).css('background-color', '#e9fbba');			  
    });  
	
    $("table#table2").find("td#table2td1").mouseleave(function() {
           // alert("hi");
		   	  $(this).css('background-color', '#effbcf');	            
    });
	
	// timelinedesc1
	$("div#gridfooter").find("div#timelinedesc1").hide();
	
	$("div#timelinedesc").find("div#timelinedescfooter1").click(function() {
        // alert("hi");
		$("div#gridfooter").find("div#timelinedesc1").show();
		$(this).hide();
		$("div#timelinedesc").find("div#timelinedescfooter").text('');
		//$("div#gridfooter").find("div#timelinedesc").css('border-bottom', '0px');
    });
    
	$("div#timelinedesc1").find("div#timelinedesc1btntop").click(function() {
        // alert("hi");
		$("div#gridfooter").find("div#timelinedesc1").hide();
		$("div#timelinedesc").find("div#timelinedescfooter1").fadeIn('slow');
		$("div#timelinedesc").find("div#timelinedescfooter").text('Above are the pre-chosen dates. Customize your own range of timeline');
		//$("div#gridfooter").find("div#timelinedesc").css('border-bottom', '1px');
    });
	
};  

function datepick(){
	
	$("#inlinedatepicker1").calendar({
	    parentElement: '#inlinedatepicker1-container',
	    dateFormat: '%d-%m-%Y'	
	});
	
	// calender for inlinedatepicker2
	$("#inlinedatepicker2").calendar({
	    parentElement: '#inlinedatepicker2-container',
	    dateFormat: '%d-%m-%Y'	
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
    gridview();
	datepick();
	timelinedesc1close();
	
});
	