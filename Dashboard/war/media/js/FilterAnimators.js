function FilterAnimators(sel_val) {
	//alert('alert message');
	var facilitatorList = $('id_facilitator');

	for (var count = facilitatorList.options.length-1; count >-1; count--){
		facilitatorList.options[count] = null;
	}
	facilitatorList.options[0] = new Option('Loading...', '-1', false, false);
	facilitatorList.disabled = true;

	var villageList = $('id_village');
	var village_id = villageList.options[villageList.selectedIndex].value;
	if (village_id > 0) {
		//alert(village_id);

		new Ajax.Request('/animators-by-village-id/' + village_id + '/', {
			method: 'get',
			onSuccess: function(transport){
				//alert("success");
				var response = transport.responseText || 'no response text';
				//alert(response);
				var kvpairs = response.split("\n");
				//alert(kvpairs);
				if(kvpairs.length <= 2)
					facilitatorList.options[0] = new Option('No facilitator','0',false,false);
				for (i=0; i<kvpairs.length - 2; i++) {
					m = kvpairs[i].split("\t");
					//alert(m[1]);
					//alert(m[0]);
					var option = new Option(m[1], m[0], false, false);
					facilitatorList.options[i] = option;
				}
				facilitatorList.disabled = false;
				if (sel_val > 0) {
					facilitatorList.value = sel_val;
				}
			},
			onFailure: function(){
				alert('An error occured trying to filter the facilitator list.');
				facilitatorList.options[0] = new Option('Other', '0', false, false);
				facilitatorList.disabled = false;
			}
		});
	}
	else {
		facilitatorList.options[0] = new Option('Select Village', '-1', false, false);
		facilitatorList.disabled = true;
	}
}
