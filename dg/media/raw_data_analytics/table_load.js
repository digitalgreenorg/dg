window.onload = table_load;

function table_load()
{               
	
	var json = $("#tablex").data("val-json");
	console.log("hello", json);
//	var parsed = JSON.parse(json);
	var formated_json = [];
	var full_data = {};
	var keyset = Object.keys(json);
	console.log("yoyo", keyset);
	console.log("yoyo2", keyset);

	var interkeys = Object.keys(json[keyset[0]])
	for (var i=0; i<interkeys.length; i++){
		var obj={};
		console.log('i',i);
		console.log('heo',Object.keys(json[keyset[0]]));
		for (var j=0; j<keyset.length;j++){
			console.log('j',keyset[j]);
			console.log('json',json[keyset[j]]);
			obj[keyset[j]] = json[keyset[j]][interkeys[i]];
		}
		formated_json.push(obj);
	}
	full_data.data = formated_json;
	console.log('yipee', full_data);

	 $('#example').DataTable( {
        "aaData": full_data,
        "aoColumns": keyset
    } );

}