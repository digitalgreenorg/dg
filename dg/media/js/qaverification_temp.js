/**
 * Created by Lokesh on 2015-03-17.
 */


function QAverification() {
    jQuery(".result-list tr").find("select").change(function () {
        if (jQuery(this).val() != 3) {
            jQuery(this).parent().parent().find('input[type="text"]').prop('disabled', false);
        }
        if (jQuery(this).val() == 3) {
            jQuery(this).parent().parent().find('input[type="text"]').val("");
            jQuery(this).parent().parent().find('input[type="text"]').prop('disabled', true);
        }
    });

    jQuery('.result-list tr').each(function () {
        if (jQuery(this).find("select option:selected").text() == "Not Checked") {
            jQuery(this).find('input[type="text"]').prop('disabled', true);
        }
    });

    jQuery("#id_verification_status").change(function () {
        if (jQuery("#id_verification_status").val() != 3) {
            jQuery("#id_verified_by").prop('disabled', false);
        }
        if (jQuery("#id_verification_status").val() == 3) {
            jQuery("#id_verified_by").val("");
            jQuery("#id_verified_by").prop('disabled', true);
        }
    });

    if (jQuery("#id_verification_status option:selected").val() == 3) {
        jQuery('#id_verified_by').prop('disabled', true);
    }

    jQuery('p[class="submit-row"] input[name="_save"]').click(function (event) {
        jQuery('.result-list tr').each(function () {
            if (jQuery(this).find('input[type="text"]').prop('disabled') != true) {
                if (jQuery(this).find('input[type="text"]').val() == "") {
                    alert("Kindly fill all the Active Verified By fields");
                    event.preventDefault();
                }
            }
        });
    });

    jQuery('div[class="submit-row"] input[name="_save"], input[name="_addanother"], input[name="_continue"]').click(function (event) {
        if (jQuery('#id_verified_by').prop('disabled')!=true){
            if(jQuery('#id_verified_by').val()==""){
                alert("Kindly fill the Verified By field");
                event.preventDefault();
            }
        }
    });
}
window.onload = QAverification;
