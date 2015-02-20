
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
  
    if((list.checked) && (video.checked))
    {
    
        listoptions.style.visibility = "visible";
    }
    else
        listoptions.style.visibility = "hidden"; 

}
//validation check
function validation_check()
{
     
     var checked_partitions = [animator, group, people, video];
     var checked_values = [screening, adoption, animator_no, attendance,video_screened_no, video_produced_no]
     var count_partition = 0;
     var count_values = 0
     var i;
     
     if(list.checked)
     {
       for(i=0; i<checked_partitions.length; i++)
          {
            if(checked_partitions[i].checked)
              {count_partition ++;}
          }
        if (count_partition >1)
        {
          alert("Along with list please select either Animator/Group/egistered Viewers/Video from Partions");
          event.preventDefault();
         
        }

     }
     //alert(list_video.selectedIndex);
     if( ((animator.checked) && (animator_no.checked))           || 
         ((people.checked)   && (animator_no.checked))           ||
         ((people.checked)   && (attendance.checked))            ||
         ((people.checked)   && (list_video.selectedIndex != 0)) ||
         ((group.checked)    && (animator_no.checked))           ||
         ((group.checked)    && (list_video.selectedIndex != 0)) ||
         ((video.checked)    && (animator_no.checked))           ||
         ((video.checked)    && (video_screened_no.checked))     ||
         ((video.checked)    && (video_produced_no.checked)))
          {
           alert("Invalid Entry!!!");
           event.preventDefault(); 
          }

     if((video.checked) && (list.checked) && (list_video.selectedIndex == 0))
     {
        alert("Please select list of videos produced or list of videos produced from dropdown!!!");
        event.preventDefault(); 

     }  

     if(list.checked)
     {
       for(i=0; i<checked_values.length; i++)
          {
            if(checked_values[i].checked)
              {count_values ++;}
          }
        if (count_values > 0)
        {
          alert("No other value fields can be selected along with list!!");
          event.preventDefault();
         
        }

     }
     
}
