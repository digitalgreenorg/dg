/**
 * Created by Lokesh on 2015-05-06.
 */


function QAscreening() {
    jQuery(".result-list tr").find("select[name$='status']").change(function () {
        if (jQuery(this).val() != 0) {
            jQuery(this).parent().parent().find("select[name$='grade']").prop('disabled', false).css('background-color', '#ffffff');
            jQuery(this).parent().parent().find("select[name$='observer']").prop('disabled', false).css('background-color', '#ffffff');
        }
        if (jQuery(this).val() == 0) {
            jQuery(this).parent().parent().find("select[name$='grade']").val("");
            jQuery(this).parent().parent().find("select[name$='grade']").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).parent().parent().find("select[name$='observer']").prop('disabled', true).val('').css('background-color', '#e0e0e0');
        }
    });

    jQuery('.result-list tr').each(function () {
        jQuery(this).find("select[name$='grade']").css('max-width','50px');
        jQuery(this).find("select[name$='status']").css('max-width','120px');
        jQuery(this).find("select[name$='observer']").css('max-width','100px');
        if (jQuery(this).find("select[name$='status'] option:selected").text() == "Not Observed") {
            jQuery(this).find("select[name$='grade']").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).find("select[name$='observer']").prop('disabled', true).css('background-color', '#e0e0e0');
        }
    });

    jQuery('p[class="submit-row"] input[name="_save"]').click(function (event) {
        jQuery('.result-list tr').each(function () {
            if (jQuery(this).find("select[name$='grade']").prop('disabled') != true) {
                if (jQuery(this).find("select[name$='observer']").val() == ""){
                    alert("Kindly fill all active \"Observer\" fields");
                    event.preventDefault();
                    return false;
                }
                if (jQuery(this).find("select[name$='grade']").val() == "") {
                    alert("Kindly fill all the active \"Screening Grade\" fields");
                    event.preventDefault();
                    return false;
                }
            }
        });
    });

    jQuery("#id_observation_status").change(function () {
        if (jQuery("#id_observation_status").val() != 0) {
            jQuery("#id_screening_grade").prop('disabled', false).css('background-color', '#ffffff');
            jQuery("#id_observer").prop('disabled', false).css('background-color', '#ffffff');
        }
        if (jQuery("#id_observation_status").val() == 0) {
            jQuery("#id_screening_grade").val("");
            jQuery("#id_screening_grade").prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery("#id_observer").prop('disabled', true).val("").css('background-color', '#e0e0e0');
        }
    });

    if (jQuery("#id_observation_status option:selected").val() == 0) {
        jQuery('#id_screening_grade').prop('disabled', true).css('background-color', '#e0e0e0');
        jQuery("#id_observer").prop('disabled', true).css('background-color', '#e0e0e0');
    }

    jQuery('div[class="submit-row"] input[name="_save"], input[name="_addanother"], input[name="_continue"]').click(function (event) {
        if (jQuery('#id_screening_grade').prop('disabled')!=true){
            if(jQuery("#id_observer").val() == ""){
                alert("Please fill the \"Observer\" field");
                event.preventDefault();
                return false;
            }

            if(jQuery('#id_screening_grade').val()==""){
                alert("Kindly fill the \"Screening Grade\" field");
                event.preventDefault();
            }
        }
    });
}
window.onload = QAscreening;
