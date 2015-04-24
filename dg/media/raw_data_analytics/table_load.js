window.onload = table_load;

function table_load()
{               
	
	var json = $("#tablex").data("val-json");
	console.log("hello", json);
//	var parsed = JSON.parse(json);
	var formated_json = [];
	var full_data = [];
	var keyset = Object.keys(json);
	console.log("yoyo", keyset);
	console.log("yoyo2", keyset);

	var interkeys = Object.keys(json[keyset[0]])
	for (var i=0; i<interkeys.length; i++){
		var obj=[];
		console.log('i',i);
		console.log('heo',Object.keys(json[keyset[0]]));
		for (var j=0; j<keyset.length;j++){
			console.log('j',keyset[j]);
			console.log('json',json[keyset[j]]);
			obj[j] = json[keyset[j]][interkeys[i]];
		}
		formated_json.push(obj);
	}
	full_data.push(formated_json);
	console.log('yipee', full_data);

	var column_arr = [];
	for(var i=0; i<keyset.length; i++)
	{
		var column_obj = {};
		column_obj["sTitle"] = keyset[i];
		column_obj["sClass"] = "a-center";
		column_arr.push(column_obj);

	}
	console.log("aocolumn", column_arr);

	jQuery('#example').dataTable( {
		"sDom":'T<"clear">lfrtip',
		"bAutoWidth":false,
        "aaData": formated_json,
        "aoColumns": column_arr,
        "oTableTools":{

            "sSwfPath": "/media/social_website/scripts/libs/tabletools_media/swf/copy_csv_xls_pdf.swf"
			}
    } );

}