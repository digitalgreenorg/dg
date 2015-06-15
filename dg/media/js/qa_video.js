/**
 * Created by Lokesh on 2015-05-06.
 */


function QAvideo() {
    jQuery(".result-list tr").find("select[name$='status']").change(function () {
        if (jQuery(this).val() != 0) {
            jQuery(this).parent().parent().find("select[name$='grade']").prop('disabled', false).css('background-color', '#ffffff');
            jQuery(this).parent().parent().find("select[name$='reviewer']").prop('disabled', false).css('background-color', '#ffffff');
        }
        if (jQuery(this).val() == 0) {
            jQuery(this).parent().parent().find("select[name$='grade']").val("");
            jQuery(this).parent().parent().find("select[name$='grade']").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).parent().parent().find("select[name$='reviewer']").prop('disabled', true).val('').css('background-color', '#e0e0e0');
        }
    });

    jQuery('.result-list tr').each(function () {
        jQuery(this).find("select[name$='status']").css('max-width','120px');
        jQuery(this).find("select[name$='grade']").css('max-width','100px');
        jQuery(this).find("select[name$='reviewer']").css('max-width','100px');
        if (jQuery(this).find("select[name$='status'] option:selected").text() == "Not Reviewed") {
            jQuery(this).find("select[name$='grade']").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).find("select[name$='reviewer']").prop('disabled', true).css('background-color', '#e0e0e0');
        }
    });

    jQuery('p[class="submit-row"] input[name="_save"]').click(function (event) {
        jQuery('.result-list tr').each(function () {
            if (jQuery(this).find("select[name$='grade']").prop('disabled') != true) {
                if (jQuery(this).find("select[name$='reviewer']").val() == ""){
                    alert("Kindly fill all active \"Reviewer\" fields");
                    event.preventDefault();
                    return false;
                }
                 if (jQuery(this).find("select[name$='grade']").val() == "") {
                    alert("Kindly fill all the active \"Video Grade\" fields");
                    event.preventDefault();
                    return false;
                }
            }
        });
    });

    jQuery("#id_review_status").change(function () {
        if (jQuery("#id_review_status").val() != 0) {
            jQuery("#id_video_grade").prop('disabled', false).css('background-color', '#ffffff');
            jQuery("#id_reviewer").prop('disabled', false).css('background-color', '#ffffff');
        }
        if (jQuery("#id_review_status").val() == 0) {
            jQuery("#id_video_grade").val("");
            jQuery("#id_video_grade").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery("#id_reviewer").prop('disabled', true).val("").css('background-color', '#e0e0e0');
        }
    });

    if (jQuery("#id_review_status option:selected").val() == 0) {
        jQuery('#id_video_grade').prop('disabled', true).css('background-color', '#e0e0e0');
        jQuery("#id_reviewer").prop('disabled', true).css('background-color', '#e0e0e0');
    }

    jQuery('div[class="submit-row"] input[name="_save"], input[name="_addanother"], input[name="_continue"]').click(function (event) {
        if (jQuery('#id_video_grade').prop('disabled')!=true){
            if(jQuery("#id_reviewer").val() == ""){
                alert("Please fill the \"Reviewer\" field");
                event.preventDefault();
                return false;
            }

             if(jQuery('#id_video_grade').val()==""){
                alert("Kindly fill the \"Video Grade\" field");
                event.preventDefault();
            }
        }
    });
}
window.onload = QAvideo;
