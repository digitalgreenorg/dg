// loading the default features of the web page


function defaultload1(){ 
			
			$('a#contendtd1divsub1link').attr('target', '_blank');
			$('div#contendtd1divsub1 a').attr('target', '_blank');					
           	// alert(1);                       
            $("img#toptableimg").fadeIn(3000);
            
            
} // function defaultload

/* This is run when the page is fully loaded */
$(document).ready(function(){	   
	defaultload1();	
});