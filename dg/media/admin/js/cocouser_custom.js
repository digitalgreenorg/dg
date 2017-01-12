window.__admin_url = '/admin/';
function addEvent(obj, evType, fn) {
	if (obj.addEventListener) {
	    obj.addEventListener(evType, fn, false);
	    return true;
	} 
	else if (obj.attachEvent) {
	    var r = obj.attachEvent("on" + evType, fn);
	    return r;
	} 
	else {
	    return false;
	}
}

function clear_villages(){
	$("#village_from")
	.find("option")
	.remove();
}

function clear_district()
{
	$("#id_district")
	.find("option")
	.remove();
}

function get_villages()
{
	district_id = $("#id_district").val();
	var selected_villages = [];
	$("#village_to")
	.find('option')
	.each(function(index,obj){
		selected_villages.push(parseInt(obj.value));
	});
	$.get("/admin/coco/cocouser/add/district_wise_village",{district_id:district_id}).done(function(village_list){
		village_list = JSON.parse(village_list);           	
		clear_villages();
		village_list = village_list.filter(function(village) { 
			return selected_villages.indexOf(village['id']) < 0;
			});
		$.each(village_list, function (index) {
			$('#village_from').append($("<option></option>")
			.attr("value",village_list[index]['id'])
			.text(village_list[index]['village_name']));
		});
		SelectBox.init("village_from");
	});
}

function get_district()
{
	state_id = $("#id_state").val();
	clear_villages();
	$.get("/admin/coco/cocouser/add/state_wise_district",{state_id:state_id}).done(function(district_list){
		district_list = JSON.parse(district_list);           	
		clear_district();
		$('#id_district').append("<option selected disabled> -- select an option -- </option>");
		$.each(district_list, function (index) {
			$('#id_district').append($("<option></option>")
			.attr("value",district_list[index]['id'])
			.text(district_list[index]['district_name']));
		});
	});
}

function check_validation(element_id)
{
	if(!($(element_id).val()))
	{
		$(element_id).parent().parent().parent().addClass("errors");
		$(element_id).parent().parent().parent().children('ul').show();
		$("#errornote").show();
		return true;
	}
	else
		return false;
}

$(document).ready(function() {
	$("form").submit(function(e){
		if(check_validation("#id_user"))
		{
			e.preventDefault(e);
		}
		else
		{
			$("#id_user").parent().parent().parent().removeClass("errors");
			$("#id_user").parent().parent().parent().children('ul').hide();
			$("#errornote").hide();
		}
		if(check_validation("#id_partner"))
		{
			e.preventDefault(e);
		}
		else
		{
			$("#id_partner").parent().parent().parent().removeClass("errors");
			$("#id_partner").parent().parent().parent().children('ul').hide();
		}
		if($("#village_to").has('option').length == 0)
		{
			e.preventDefault(e);
			$("#village_to").parent().parent().parent().addClass("errors");
			$("#village_to").parent().parent().parent().parent().children('ul').show();
			$("#errornote").show();
		}
		else
		{
			$("#village_to").parent().parent().parent().removeClass("errors");
			$("#village_to").parent().parent().parent().parent().children('ul').hide();
		}
	});
});
