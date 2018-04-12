// function to choose the dates 

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
    
    // timelinedesc1	
	
	$("div#timelinedesc").find("div#timelinedescfooter1").click(function() {
        $("div#gridfooter").find("div#timelinedesc1").show();
		$(this).hide();
		$("div#timelinedesc").find("div#timelinedescfooter").text('');		
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

// called when one clicks the hide button of the timelinedesc1 div
function timelinedesc1close(){

 $("div#timelinedesc1").hide();
 $("div#timelinedesc").find("div#timelinedescfooter1").fadeIn('slow');
 $("div#timelinedesc").find("div#timelinedescfooter").text('Above are the pre-chosen dates. Customize your own range of timeline');   
};


/** This run when the body page is fully loaded */
$(document).ready(function(){    
	datepick();	
	timelinedesc1close();	
});
