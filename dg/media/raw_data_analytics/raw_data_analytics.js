
//window.onload = list_display;
//###############################Populate the dropdowns for filter######################################
function statechange(src, val) 
{			
	$.get( "/raw_data_analytics/dropdown_state/", { selected : val })
           .done(function( data ) {
               data_json = JSON.parse(data);
               $('#stateID ').find('option:gt(0)').remove();
               $('#districtID ').find('option:gt(0)').remove();
               $('#blockID ').find('option:gt(0)').remove();
               $('#villageID ').find('option:gt(0)').remove();
                for (i in data_json){
                   	$('#stateId').append("<option>"+data_json[i]+"</option>");
               }
           });
}

function districtchange(src, val) 
{				
	$.get( "/raw_data_analytics/dropdown_district/", { selected : val })
           .done(function( data ) {
               data_json = JSON.parse(data);
               $('#districtID ').find('option:gt(0)').remove();
               $('#blockID ').find('option:gt(0)').remove();
               $('#villageID ').find('option:gt(0)').remove();
               for (i in data_json){
               		$('#districtId').append("<option>"+data_json[i]+"</option>");
               }
           });
}

function blockchange(src, val) 
{			
	$.get( "/raw_data_analytics/dropdown_block/", { selected : val })
           .done(function( data ) {
               data_json = JSON.parse(data);
               $('#blockID ').find('option:gt(0)').remove();
               $('#villageID ').find('option:gt(0)').remove();                  
               for (i in data_json){
               		$('#blockId').append("<option>"+data_json[i]+"</option>");
        
               }
           });
}

function villagechange(src, val) 
{				
	$.get( "/raw_data_analytics/dropdown_village/", { selected : val })
           .done(function( data ) {
               data_json = JSON.parse(data);
               $('#villageID ').find('option:gt(0)').remove();
               for (i in data_json){
            		$('#villageId').append("<option>"+data_json[i]+"</option>");
               }
           });
}
//##################################################################################################################

function list_display()
{
  
    if((list.checked) && (video_chk.checked))
    {
    
        listoptions.style.visibility = "visible";
    }
    else
        listoptions.style.visibility = "hidden"; 

}
//validation check
function validation_check()
{
     
     var checked_ids = [animator_chk, group_chk, people_chk, video_chk];
     var count = 0;
     var i;
     
     if(list.checked)
     {
       for(i=0; i<checked_ids.length; i++)
          {
            if(checked_ids[i].checked)
              {count ++;}
          }
        if (count >1)
        {
          alert("Along with list please select either Animator, Group, Registered Viewers or Video.");
          event.preventDefault();
         
        }

     }
}
