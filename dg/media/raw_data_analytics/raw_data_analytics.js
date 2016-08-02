window.onload = date;

/*$(document).ready(function() {
 var cur_date = new Date();
 $('#date').val(cur_date);
 alert(cur_date);
 });*/
//###############################Populate the dropdowns for filter######################################

function statepopulate(src, val) {

    $('#districtID ').find('option').remove();
    $('#blockID ').find('option').remove();
    $('#villageID ').find('option').remove();

    $('#villageId ').trigger('chosen:updated');
    $('#blockId ').trigger('chosen:updated');
    $('#districtId ').trigger('chosen:updated');
    for (var j in val) {
        $.get("/raw_data_analytics/dropdown_" + src + "/", {selected: val[j]})
            .done(function (data) {
                data_json = JSON.parse(data);


                for (var i in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[i] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[i] + '">' + data_json[i] + '</option>');

                }

            });

    }

}


function districtpopulate(src, val) {
    $('#blockID ').find('option').remove();
    $('#villageID ').find('option').remove();
    $('#villageId').trigger('chosen:updated');
    $('#blockId').trigger('chosen:updated')
    for (var j in val) {
        $.get("/raw_data_analytics/dropdown_" + src + "/", {selected: val[j]})
            .done(function (data) {
                data_json = JSON.parse(data);

                ;
                for (var i in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[i] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[i] + '">' + data_json[i] + '</option>');

                }

            });

    }
}

function blockpopulate(src, val) {
    $('#villageID ').find('option').remove();
    $('#villageId ').trigger('chosen:updated');
    for (var j in val) {
        $.get("/raw_data_analytics/dropdown_" + src + "/", {selected: val[j]})
            .done(function (data) {
                data_json = JSON.parse(data);

                for (var i in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[i] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[i] + '">' + data_json[i] + '</option>');

                }

            });

    }
}

function villagepopulate(src, val) {
    for (var j in val) {
        $.get("/raw_data_analytics/dropdown_" + src + "/", {selected: val[j]})
            .done(function (data) {
                data_json = JSON.parse(data);

                for (var i in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[i] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[i] + '">' + data_json[i] + '</option>');

                }

            });

    }
}
function videopopulate(src, val) {
    for (var j in val) {
        $.get("/raw_data_analytics/dropdown_" + src + "/", {selected: val[j]})
            .done(function (data) {
                data_json = JSON.parse(data);
                //  console.log(data_json);
                /*$('#stateID ').find('option:gt(0)').remove();
                 $('#districtID ').find('option:gt(0)').remove();
                 $('#blockID ').find('option:gt(0)').remove();
                 $('#villageID ').find('option:gt(0)').remove();*/

                for (var i in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[i] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[i] + '">' + data_json[i] + '</option>');

                }

            });

    }
}
//##################################################################################################################

function list_display() {

    if ((list.checked) && (video.checked)) {

        listoptions.style.visibility = "visible";
    }
    else
        listoptions.style.visibility = "hidden";

}
//validation check
function validation_check() {
    var error = 0;
    var checked_partitions = [partner, country, state, district, block, village]
    var checked_partitions_restrict = [animator, group, people, video];
    var checked_values = [screening, adoption, animator_no, attendance, video_screened_no, video_produced_no]
    var count_partition_restrict = 0;
    count_partition = 0;
    var count_values = 0;
    var i;

    for (i = 0; i < checked_partitions.length; i++) {

        if (checked_partitions[i].checked) {
            console.log(checked_partitions[i]);
            count_partition++;
        }
    }
    for (i = 0; i < checked_values.length; i++) {
        if (checked_values[i].checked) {
            count_values++;
        }
    }

    if ((count_partition == 0) && (count_values == 0) && (count_partition_restrict == 0) && (!list.checked)) {
        alert("Please select some fields !!");
        event.preventDefault();
    }

    else if ((count_partition != 0) && (count_values == 0) && (!list.checked)) {
        alert("Please select atleast one value field!!");
        event.preventDefault();

    }


    if (list.checked) {
        for (i = 0; i < checked_partitions_restrict.length; i++) {
            if (checked_partitions_restrict[i].checked) {
                count_partition_restrict++;
            }
        }
        if (count_partition_restrict > 1) {
            alert("Along with list please select either Animator/Group/Registered Viewers/Video from Partitions");
            error = 1;
            event.preventDefault();

        }

        else if ((count_partition_restrict == 0) && (count_partition == 0)) {
            alert("Select atleast one option from partition fields!!!");
            error = 1;
            event.preventDefault();

        }


    }
    //alert(list_video.selectedIndex);
    if (((animator.checked) && (animator_no.checked)) ||
        ((people.checked) && (animator_no.checked)) ||
        ((people.checked) && (attendance.checked)) ||
        ((group.checked) && (animator_no.checked)) ||
        ((video.checked) && (animator_no.checked)) ||
        ((video.checked) && (video_screened_no.checked)) ||
        ((video.checked) && (video_produced_no.checked))) {
        alert("Invalid combination of 'Value' and 'Partition' fields!! Please check");
        error = 1;
        event.preventDefault();
    }

    if ((video.checked) && (list.checked) && (list_video.selectedIndex == 0)) {
        alert("Please select list of videos produced or list of videos produced from dropdown!!!");
        error = 1;
        event.preventDefault();

    }

    if (list.checked) {
        if (count_values > 0) {
            alert("No other value fields can be selected along with list!!");
            error = 1;
            event.preventDefault();

        }

    }


}
//#######################################onload-date################################################
function date() {
    date = new Date();
    document.getElementById('to_date').valueAsDate = date;
    date.setMonth(date.getMonth() - 1);
    document.getElementById('from_date').valueAsDate = date;
}
