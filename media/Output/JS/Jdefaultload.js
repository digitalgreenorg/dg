// loading the default features of the web page


function defaultload(){ 
			
 // navigation search bar
			$("input#navsearchinput").focus(function() {  
         		if (this.value == this.defaultValue || this.value != this.defaultValue){  
             		this.value = '';  
         		}         		  
     		});  
    		$("input#navsearchinput").blur(function() {  
         	    if ($.trim(this.value == '')){  
               		this.value = (this.defaultValue ? this.defaultValue : '');  
         	    }  
     		}); 
     		
 // applying border to link in the pagination div of press column
     		$("#pagingdivul li").mouseover(function() {            	
            	$(this).css('border-color','#5B6E1D');
            });
            
            $("#pagingdivul li").mouseleave(function() {            	
            	$(this).css('border-color','#E7F7CF');
            }); 	
            
            
// navigation header panel that has the sub menus like About, News, etc
            
            $("div#headmenu1").mouseover(function() {            	
            	$(this).find("div#subheadmenu1").show();
            });
            
            $("div#headmenu1").mouseleave(function() {            	
            	$(this).find("div#subheadmenu1").hide();
            });           
  
// the help bubbles for different titles on the analytics and overview pages 
                   
            $("div#headermenutitlename").mouseover(function() {            	
            	$(this).css('color','#ffffff');            	
            	//$(this).css('border-bottom-width','3px');            	
            	//$(this).css('background-color','#ffffff');
            	$(this).find('#subheadmenutop').show();
            	$(this).find('#subheadmenu').show();            	
            }); 
            
            $("div#headermenutitlename").mouseleave(function() {            	
            	$(this).css('color','#ffffff');            	
            	//$(this).css('border-bottom-width','0px');
            	//$(this).css('background-color','transparent');            	
            	$(this).find('#subheadmenutop').hide();
            	$(this).find('#subheadmenu').hide();
            });
            
// changing the text colour and background colour attributes on mouseover over sublinks to the header menu like About Us, News             
            $("#subheadmenulist li a").mouseover(function() {            	
            	$(this).css('color','#ffffff');
            	$(this).css('background-color','#59af04');
            });
            
            $("#subheadmenulist li a").mouseleave(function() {            	
            	$(this).css('color','#000000');
            	$(this).css('background-color','#ecf3c9');
            });
            
            
// Calender Default Settings 
                                   
            $("div#inlinedatepicker1").calendar({	       		
	       		dateFormat:"%Y-%m-%d",	       		
			});
			
			$("div#inlinedatepicker2").calendar({	       		
	       		dateFormat:"%Y-%m-%d",	
			});			            
      
         
} // function defaultload

/* This is run when the page is fully loaded */
$(document).ready(function(){	   
	defaultload();	
});