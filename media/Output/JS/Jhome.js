// loading the default features of the web page

function defaultload1(){ 
			
			//$('a#contendtd1divsub1link').attr('target', '_blank');
			//$('div#contendtd1divsub1 a').attr('target', '_blank');					
           	// alert(1);                       
            $("img#toptableimg").fadeIn(3000);
           
           // closing the video overlay 
            $("div#overlaydivvideodesc2").click( function(){			
        		$("div#overlaydiv").fadeOut(1000);        		  			
			});
                        
} // function defaultload

function displayvideo(n){

	$('div#overlaydiv').fadeIn(1000); 
	var e = document.getElementById('overlaydivvideoembed');	
	var e2 = document.getElementById('overlaydivvideodesc1');	
	
	
	var xmlDoc=null;
    if (window.XMLHttpRequest)
    {
    	xhttp=new XMLHttpRequest();
    }
    else 
    {
    	xhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    xhttp.open("GET","/media/Output/homeimg.xml",false);
    xhttp.send();
    xmlDoc=xhttp.responseXML;
								
	if (xmlDoc!=null) 
	{
		var x=xmlDoc.getElementsByTagName("TEAM");
		var e = document.getElementById('overlaydivvideoembed');
		e.innerHTML = "<object width='100%' height='100%'><param name='movie' value='" +  (x[n].getElementsByTagName('VIDEOLINK')[0].childNodes[0].nodeValue) + "'></param><param name='allowFullScreen' value='true'></param> <param name='allowscriptaccess' value='always'></param><param name='wmode' value='transparent'/><embed src='" + (x[n].getElementsByTagName('VIDEOLINK')[0].childNodes[0].nodeValue) + " type='application/x-shockwave-flash' allowscriptaccess='always' allowfullscreen='true' width='100%' height='100%' wmode='transparent'></embed></object>";
						
		e2.innerHTML = x[n].getElementsByTagName("PLACE")[0].childNodes[0].nodeValue;
	}		
	
}


/* This is run when the page is fully loaded */
$(document).ready(function(){	   
	defaultload1();	
});