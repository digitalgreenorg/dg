window.onload = table_load;

function table_load()
{               
	
	var json = $("#tablex").data("val-json");
	
	var formated_json = [];
	var full_data = [];
	var keyset = Object.keys(json);
	var interkeys = Object.keys(json[keyset[0]]);
	var customTitle='rawdata_'
	var d = new Date();
	customTitle= customTitle + d.getFullYear()+d.getMonth()+d.getDay()+'T'+d.getHours()+d.getMinutes();
	for (var i=0; i<interkeys.length; i++){
		var obj=[];
		for (var j=0; j<keyset.length;j++){
			obj[j] = json[keyset[j]][interkeys[i]];
		}
		formated_json.push(obj);
	}
	full_data.push(formated_json);
	
	var column_arr = [];
	for(var i=0; i<keyset.length; i++)
	{
		var column_obj = {};
		column_obj["sTitle"] = keyset[i];
		column_obj["sClass"] = "a-center";
		column_arr.push(column_obj);

	}
	
	$('#example').dataTable( {
		"sDom":'T<"bottom"B><"clear">lf<"clear">i',
		"AutoWidth":false,
        "aaData": formated_json,
        "aoColumns": column_arr,
        "swfPath" : "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls.swf",
        "buttons": [
        	
        {
            "extend": 'copyHtml5',
            "text": 'Copy to Clipboard',
            "title":customTitle
        },
        {
        	"extend": 'excelHtml5',
            "text": 'Download in Excel',
            "title":customTitle
        }
    ]
    } );
	$('.dt-buttons').css('float','right');
}