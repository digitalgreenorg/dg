/**
 * Created by Lokesh on 2015-05-06.
 */


function QAverification() {
    jQuery(".result-list tr").find("select[name$='status']").change(function () {
        if (jQuery(this).val() != 0) {
            if(jQuery(this).val() == 1){
                jQuery(this).parent().parent().find("input[name$='check']").prop('checked', false).prop('disabled', false).css('background-color', '#ffffff');
                jQuery(this).parent().parent().find("select[name$='verified_by']").prop('disabled', false).css('background-color', '#ffffff');
            }
            if(jQuery(this).val() == 2){
                jQuery(this).parent().parent().find("input[name$='check']").prop('checked', false).prop('disabled', false).css('background-color', '#ffffff');
                jQuery(this).parent().parent().find("select[name$='verified_by']").prop('disabled', false).css('background-color', '#ffffff');
            }
        }
        if (jQuery(this).val() == 0) {
            jQuery(this).parent().parent().find("input[name$='check']").prop('checked',false).prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).parent().parent().find("select[name$='verified_by']").prop('disabled', true).val('').css('background-color', '#e0e0e0');
        }
    });

    jQuery('.result-list tr').each(function () {
        jQuery(this).find("ul").css('width','150px');
        jQuery(this).find("li").css('display','inline');
        jQuery(this).find("select[name$='status']").css('max-width','120px');
        jQuery(this).find("select[name$='verified_by']").css('max-width','100px');
        if (jQuery(this).find("select[name$='status'] option:selected").text() == "Not Checked") {
            jQuery(this).find("input[name$='check']").prop('checked',false).prop('disabled', true).css('background-color', '#e0e0e0');
            jQuery(this).find("select[name$='verified_by']").prop('disabled', true).css('background-color', '#e0e0e0');
        }
    });



    jQuery('p[class="submit-row"] input[name="_save"]').click(function (event) {
        var flag = 0;
        jQuery('.result-list tr').each(function () {
            if (jQuery(this).find("input[name$='check']").prop('disabled') != true) {
                if (jQuery(this).find("select[name$='verified_by']").val() == ""){
                    alert("Kindly fill all active \"Verified By\" fields");
                    event.preventDefault();
                    return false;
                }
                if (jQuery(this).find("select[name$='status'] option:selected").text() == "Approved") {
                    jQuery(this).find("input[name$='check']").each(function () {
                        if (!this.checked) {
                            flag = 1;
                            alert("Kindly select all \"checkboxes\" for \"Approved Verification\" fields");
                            event.preventDefault();
                            return false;
                        }
                    });
                }
            }
            if(flag>0){
                return false
            }
        });
    });

    jQuery('input[name="non_negotiable_check" ]').css('margin','0 0 0 0px');

    jQuery("#id_verification_status").change(function () {
        if (jQuery("#id_verification_status").val() != 0) {
            if (jQuery("#id_verification_status").val() == 1){
                jQuery("input[name='non_negotiable_check']").prop('disabled', false).prop('checked', false).css('background-color', '#ffffff');
                jQuery("select[name='verified_by']").prop('disabled', false).css('background-color', '#ffffff');
            }
            if (jQuery('#id_verification_status').val() == 2){
                jQuery("input[name='non_negotiable_check']").prop('checked',false).prop('disabled', false).css('background-color', '#ffffff');
                jQuery("select[name='verified_by']").prop('disabled', false).css('background-color', '#ffffff');
            }
        }
        if (jQuery("#id_verification_status").val() == 0) {
            jQuery("input[name='non_negotiable_check']").prop('checked',false).prop('disabled',true).css('background-color', '#e0e0e0');
            jQuery("select[name='verified_by']").prop('disabled', true).val("").css('background-color', '#e0e0e0');
        }
    });

    if (jQuery("#id_verification_status option:selected").val() == 0) {
        jQuery("input[name='non_negotiable_check']").prop('disabled', true).css('background-color', '#e0e0e0');
        jQuery("select[name='verified_by']").prop('disabled', true).css('background-color', '#e0e0e0');
    }

    jQuery('div[class="submit-row"] input[name="_save"], input[name="_addanother"], input[name="_continue"]').click(function (event) {
        if (jQuery("input[name='non_negotiable_check']").prop('disabled')!=true){
            if(jQuery("#id_verified_by").val() == ""){
                alert("Please fill the \"Verified By\" field");
                event.preventDefault();
                return false;
            }

            if(jQuery("#id_verification_status").val() == 1){
                jQuery("input[name='non_negotiable_check']").each(function(){
                    if(!this.checked){
                        alert("Kindly select all \"Check boxes\"");
                        event.preventDefault();
                        return false;
                    }
                });
            }
        }
    });
}
window.onload = QAverification;