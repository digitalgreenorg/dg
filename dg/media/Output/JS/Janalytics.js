
var tchartwidth = 0.85*(0.9*(screen.width));
var tchartheight  = 400;

/* This is run when the page is fully loaded */
$(document).ready(function(){	
     
         
	// Analytics Navigation
	
	$("div#analyticsnavdiv").mouseover(function() {            	
       	$(this).find("div#analyticsnav1").show();            	
     });
     
     $("div#analyticsnavdiv").mouseleave(function() {            	
       	$(this).find("div#analyticsnav1").hide();            	
     });
     
     	
	// the analytics -> overview part
	 $("div#statdescimg").mouseover(function() {            	
       	$(this).find("div#statdescimg1").show();            	
     });
            
     $("div#statdescimg").mouseleave(function() {            	
      	$(this).find("div#statdescimg1").hide();             	
     });
     
     $("div#divtitleimg").mouseover(function() {            	
       	$(this).find("div#statdescimg1").show();
       	$(this).find("div#statdescimg2").show();
       	            	
     });
            
     $("div#divtitleimg").mouseleave(function() {            	
      	$(this).find("div#statdescimg1").hide();
      	$(this).find("div#statdescimg2").show();             	
     });            
            
      $("#arrowdown").click(function() {             	          	
        	$(this).hide();        	
           	$("#arrowup").show();
           	$("div#calenderbody").show();            	            	           	
      });         
			
	 $("div#content2tdtitle1").find("div#content2tdtitleimg").click(function() {     	
      	$("div#content2tdtitle1").find("table#content2desc1").show(); 
      	$(this).hide();     	         	            	
     });

     
     $("table#content2desc1").find("div#content2descclose").click(function() {     	
      	$("div#content2tdtitle1").find("div#content2tdtitleimg").show(); 
      	$("table#content2desc1").hide();     	         	            	
     });


	$("div#content2tdtitle2").find("div#content2tdtitleimg").click(function() {     	
      	//alert("hi");
      	$("div#content2tdtitle2").find("table#content2desc2").show(); 
      	$(this).hide();     	         	            	
     });

     
     $("table#content2desc2").find("div#content2descclose").click(function() {     	
      	$("div#content2tdtitle2").find("div#content2tdtitleimg").show(); 
      	$("table#content2desc2").hide();     	         	            	
     });
     
     $("div#content2tdtitle3").find("div#content2tdtitleimg").click(function() {     	
      	//alert("hi");
      	$("div#content2tdtitle3").find("table#content2desc3").show(); 
      	$(this).hide();     	         	            	
     });

     
     $("table#content2desc3").find("div#content2descclose").click(function() {     	
      	$("div#content2tdtitle3").find("div#content2tdtitleimg").show(); 
      	$("table#content2desc3").hide();     	         	            	
     });
     
     $("div#contentsitemap").find("div#content2tdtitleimg").click(function() {     	
      	//alert("hi");
      	 $("div#contentsitemap").css('background-color','#E8F7BA');
      	$("div#contentsitemap").find("div#sitemapdiv").show();
      	$("div#contentsitemap").find("div#content2tdtitleimgclose").show(); 
      	$(this).hide();      	
      	     	         	            	
     });
     
     $("div#contentsitemap").find("div#content2tdtitleimgclose").click(function() {     	
      	//alert("hi");
      	 $("div#contentsitemap").css('background-color','transparent');
      	$("div#contentsitemap").find("div#sitemapdiv").hide(); 
      	$(this).hide(); 
      	$("div#contentsitemap").find("div#content2tdtitleimg").show();     	
      	     	         	            	
     });
     	
});
           