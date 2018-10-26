
//####################################Form Ready#######################################

  jQuery(document).ready(function ($) {
    
    $('#partnerId').chosen({});
    $('#countryId').chosen({});
    $('#stateId').chosen({});
    $('#districtId').chosen({});
    $('#blockId').chosen({});
    $('#villageId').chosen({});
    $('#videoId').chosen({});
    $('#categoryId').chosen({});
    $('#subcategoryId').chosen({});
    $('#videopId').chosen({});
    $('#tagId').chosen({});
    $('#blocknumber_video').chosen();
    $('#villagenumber_video').chosen();
    $('#list_video').chosen();
    $('#tagId').chosen();
    $('#subcategoryId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
    $('#videopId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
      

    $('#resetId').click(function () {

        $('#partnerId').val('').trigger("chosen:updated");
        $('#countryId').val('').trigger("chosen:updated");
        $('#categoryId').val('').trigger("chosen:updated");
        $('#tagId').val('').trigger("chosen:updated");
    
        $('#stateId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#districtId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#blockId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#villageId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#videoId').find('option').remove().end().val('').prop('disabled', false).trigger("chosen:updated");
        //$('#categoryId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#subcategoryId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $('#videopId').find('option').remove().end().val('').prop('disabled', true).trigger("chosen:updated");
        $("#formId").each(function () {
            this.reset();
        });
        
    });
    $('#formId').keypress(function (event) {

        if (event.keyCode === 10 || event.keyCode === 13)
            event.preventDefault();

    });

    $("#partnerId").bind("change", function () {
        $('#videoId').find('option').remove();
        $("#videoId").prop('disabled',false);
        $("#videoId").val('').trigger("chosen:updated");
        $("#categoryId").prop('disabled',true);
        $("#categoryId").val('').trigger("chosen:updated");
        $("#categoryID").find('option').remove();
        $("#subcategoryId").prop('disabled',true);
        $("#subcategoryId").val('').trigger("chosen:updated");
        $("#subcategoryId").find('option').remove();
        $("#videopId").prop('disabled',true);
        $("#videopId").val('').trigger("chosen:updated");
        $("#videopId").find('option').remove();
        $("#tagId").prop('disabled',true);
        $("#tagId").val('').trigger("chosen:updated");
        $("#tagId").find('option').remove();
    });
    $("#videoId").bind("change", function(){
        $("#categoryId").prop('disabled',true);
        $("#categoryId").val('').trigger("chosen:updated");
        $("#categoryID").find('option').remove();
        $("#subcategoryId").prop('disabled',true);
        $("#subcategoryId").val('').trigger("chosen:updated");
        $("#subcategoryId").find('option').remove();
        $("#videopId").prop('disabled',true);
        $("#videopId").val('').trigger("chosen:updated");
        $("#videopId").find('option').remove();
        $("#tagId").prop('disabled',true);
        $("#tagId").val('').trigger("chosen:updated");
        $("#tagId").find('option').remove();
    });
    $("#categoryId").bind("change",function (){
        $("#subcategoryId").find('option').remove();
        $("#subcategoryId").prop('disabled',false);
        $("#subcategoryId").val('').trigger("chosen:updated"); 
        $("#videopId").find('option').remove();
        $("#videopId").prop('disabled',true);
        $("#videopId").val('').trigger("chosen:updated");
        $("#tagId").find('option').remove();
        $("#tagId").prop('disabled',false);
        $("#tagId").val('').trigger("chosen:updated");
        
        
    });
    $("#subcategoryId").bind("change",function(){
        $('#videopId').prop('disabled',false);
        $('#videopId').find('option').remove();
        $('#videopId').val('').trigger("chosen:updated");
        $('#tagId').find('option').remove();
        $('#tagId').val('').trigger("chosen:updated");
        $('#tagId').prop('disabled',false);
    });
    $('#countryId').bind("change", function () {
        $("#partnerId").find('option').remove();
        $("#partnerId").val('').trigger('chosen:updated');
        $('#stateId').prop('disabled', false);
        $('#stateId').find('option').remove();
        $("#stateId").val('').trigger("chosen:updated");
        $('#videoId').find('option').remove();
        $("#videoId").val('').trigger("chosen:updated");
        $("#districtId").find('option').remove();
        $("#districtId").prop('disabled',true);
        $("#districtId").val('').trigger("chosen:updated");
        $("#blockId").find('option').remove();
        $("#blockId").prop('disabled',true);
        $("#blockId").val('').trigger("chosen:updated");
        $("#villageId").prop('disabled',true);
        $("#villageId").val('').trigger("chosen:updated");
        $("#villageId").find('option').remove();
    });
    $("#stateId").bind("change", function () {
        $("#districtId").find('option').remove();
        $("#districtId").prop('disabled', false);
        $("#districtId").val('').trigger("chosen:updated");
        $("#villageId").find('option').remove();
        $("#partnerId").find('option').remove();
        $("#partnerId").val('').trigger('chosen:updated'); 
        $('#videoId').find('option').remove();
        $("#videoId").val('').trigger("chosen:updated");
        $("#blockId").prop('disabled',true);
        $("#villageId").prop('disabled',true);
        $("#blockId").find('option').remove();
        $("#blockId").val('').trigger("chosen:updated");
        $("#villageId").val('').trigger("chosen:updated");
    });
    $("#districtId").bind("change", function () {
        $("#blockId").prop('disabled', false);
        $("#blockId").find('option').remove();
        $("#villageId").find('option').remove();
        $("#partnerId").find('option').remove();
        $("#partnerId").val('').trigger('chosen:updated');
        $("#blockId").val('').trigger("chosen:updated");
        /*$('#videoId').find('option').remove();
        $("#videoId").val('').trigger("chosen:updated");*/
        $("#villageId").prop('disabled',true);
        $("#villageId").val('').trigger("chosen:updated");

    });
    $("#blockId").bind("change", function () {
        $("#villageId").prop('disabled', false);
        $("#villageId").find('option').remove();
        $("#partnerId").find('option').remove();
        $("#partnerId").val('').trigger('chosen:updated');
        $("#villageId").val('').trigger("chosen:updated");
        /*$('#videoId').find('option').remove();
        $("#videoId").val('').trigger("chosen:updated");*/

    });
    $('villageId').bind("change",function () {
        $('#videoId').find('option').remove();
        $("#videoId").val('').trigger("chosen:updated");
    });
    $("#partnerId").next().bind("click",function(){
        populate_partner('partner');
        $("#partnerId").trigger("chosen:updated");
    });
    $("#stateId").next().bind("click", function () {
        populate('state', $("#countryId").val());
        $("#stateId").trigger("chosen:updated");
    });
    $("#districtId").next().bind("click", function () {
        populate("district", $("#stateId").val());
        $("#districtId").trigger("chosen:updated");
    });
    $("#blockId").next().bind("click", function () {
        populate("block", $("#districtId").val());
        $("#blockId").trigger("chosen:updated");
    });
    $("#villageId").next().bind("click", function () {
        populate("village", $("#blockId").val());
        $("#villageId").trigger("chosen:updated");
    });
    $("#videoId").next().bind("click", function () {
        populate_video("video");
        $("#videoId").trigger("chosen:updated");
    });
    $("#categoryId").next().bind("click", function () {
        populate_category("category");
        $("#categoryId").trigger("chosen:updated");
    });
    $("#subcategoryId").next().bind("click", function () {
        populate("subcategory",$('#categoryId').val());
        $("#subcategoryId").trigger("chosen:updated");
    });
    $("#videopId").next().bind("click", function () {
        populate("videop",$('#subcategoryId').val());
        $("#videopId").trigger("chosen:updated");
    });
    $("#tagId").next().bind("click", function () {
        populate_tag("tag");
        $("#tagId").trigger("chosen:updated");
    });

});
//###############################Populate the dropdowns for filter######################################




function populate(src, prevValue) {
    if (!(jQuery("#" + src + "Id" + " option ").length != 0))
        $.get("/coco/rda/dropdown_" + src + "/", {selected: prevValue})
            .always(function(){
            })
            .done(function (data) {

                data_json = JSON.parse(data);
                for (var jsonData in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[jsonData] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[jsonData] + '">' + data_json[jsonData] + '</option>');
                }
            });
}
function populate_video(src){
    prevValue= {
        "country[]":$("#countryId").val(),
        "partner[]":$("#partnerId").val(),
        "state[]":$("#stateId").val(),
        "district[]":$("#districtId").val(),
        "block[]":$("#blockId").val(),
        "village[]":$("#villageId").val()
    }
  if (!(jQuery("#" + src + "Id" + " option ").length != 0))
      $.get("/coco/rda/dropdown_video/", prevValue)
          .done(function (data) {
              data_json = JSON.parse(data);
              for (var jsonData in data_json) {
                  if (jQuery("#" + src + "Id" + " option[value='" + data_json[jsonData][0].replace("'", "").replace("'","") + "']").length == 0)
                      $("#" + src + "Id").append('<option value="' + data_json[jsonData][0] + '">' + data_json[jsonData][0]+' ( '+data_json[jsonData][1]+' )' +'</option>');
              }
          });
}

function populate_partner(src){
    prevValue = {
        "country[]":$("#countryId").val(),
        "state[]":$("#stateId").val(),
        "district[]":$("#districtId").val(),
        "block[]":$("#blockId").val(),
        "village[]":$("#villageId").val()
}
    if(!(jQuery("#partnerId option").length!=0))
        $.get("/coco/rda/dropdown_partner",prevValue)
            .done(function(data){
                data_json =JSON.parse(data);
                for(var jsonData in data_json){
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[jsonData][0] + "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[jsonData][0] + '">' + data_json[jsonData][0] + '</option>');
                }
            });
}

function populate_category(src){
    prevValue = {}

    if (!(jQuery("#categoryId  option ").length != 0))
        $.get("/coco/rda/dropdown_category", prevValue)
            .done(function (data) {
                data_json = JSON.parse(data);
                for (var jsonData in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[jsonData].replace("'", "").replace("'","")+ "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[jsonData]+ '">' + data_json[jsonData] +'</option>');
                }
            });
}

function populate_tag(src){
    prevValue = {}

    if (!(jQuery("#tagId  option ").length != 0))
        $.get("/coco/rda/dropdown_tag", prevValue)
            .done(function (data) {
                data_json = JSON.parse(data);
                for (var jsonData in data_json) {
                    if (jQuery("#" + src + "Id" + " option[value='" + data_json[jsonData]+ "']").length == 0)
                        $("#" + src + "Id").append('<option value="' + data_json[jsonData] + '">' + data_json[jsonData] +'</option>');
                }
            });
}
//##################################################################################################################


function dropdown_control(src){
    var dropdown_list = {
        "list":[list,listoptions],
        "villagenum":[villagenum,villagenumberoptions],
        "blocknum":[blocknum,blocknumberoptions]
    }

    if(src!='None' && dropdown_list[src][0].checked && (video.checked)) {
        $('#'+src).parent().siblings().children().attr('checked',false);
        dropdown_list[src][1].style.visibility ="visible";
        for (dropdown in dropdown_list){
            if(dropdown!=src)
                dropdown_list[dropdown][1].style.visibility="hidden";
        }
    }
    else {
        dropdown_list[src][1].style.visibility ="hidden";
    }

}

//validation check
function validation_check() {
    var error = 0;
    var checked_partitions = [partner, country, state, district, block, village]
    var checked_partitions_restrict = [animator, group, people];
    var checked_values = [screening, adoption, animator_no, attendance, video_screened_no, video_produced_no,blocknum,villagenum]
    var count_partition_restrict = 0;
    var count_partition = 0;
    var count_values = 0;
    var i;

    for (i = 0; i < checked_partitions.length; i++) {

        if (checked_partitions[i].checked) {
            count_partition++;
        }
    }
    for (i = 0; i < checked_values.length; i++) {
        if (checked_values[i].checked) {
            count_values++;
        }
    }

    if((!list.checked) && (count_values ==0)){
        if(count_partition==0 && count_partition_restrict==0){
            alert("Please select some fields !!");
            event.preventDefault();    
        }
        else if(count_partition!=0){
            alert("Please select atleast one value field!!");
            event.preventDefault();
        }
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
        ((video.checked) && (video_produced_no.checked))
        ||((village.checked)&&(villagenum.checked))||
        ((block.checked)&&(blocknum.checked)) ) {
        alert("Invalid combination of 'Value' and 'Partition' fields!! Please check");
        error = 1;
        event.preventDefault();
    }
    if((video.checked) && (blocknum.checked) && (blocknumber_video.selectedIndex == 0)){
        alert("Please select number of villages for screening  or number of villages for adoption from dropdown!!!");
        error = 1;
        event.preventDefault();
    }

    if ((video.checked) && (list.checked) && (list_video.selectedIndex == 0)) {
        alert("Please select list of videos produced or list of videos produced from dropdown!!!");
        error = 1;
        event.preventDefault();

    }

    if (list.checked && count_values > 0) {
            alert("No other value fields can be selected along with list!!");
            error = 1;
            event.preventDefault();
    
    }
    
}
//#######################################onload-date################################################


$(function() {
    $('input[name="daterange"]').daterangepicker({
        opens: 'right',
        locale: {
            format: 'DD/MM/YYYY'
        }
    });
});
                    