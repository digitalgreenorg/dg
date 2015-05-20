/**
 * Created by Lokesh on 2015-03-17.
 */

function QAverification() {
    jQuery("#id_verification_status").change(function () {
        if (jQuery("#id_verification_status").val() != 0) {
            jQuery(this).parent().parent().parent().parent().find('textarea').prop('disabled', false);
        }
        if (jQuery("#id_verification_status").val() == 0) {
            jQuery(this).parent().parent().parent().parent().find('textarea').val("");
            jQuery(this).parent().parent().parent().parent().find('textarea').prop('disabled', true);
        }
    });

    if (jQuery("#id_verification_status option:selected").val() == 0) {
        jQuery("#id_verification_status").parent().parent().parent().parent().find('textarea').prop('disabled', true);
    }

    if (jQuery("#id_adoptioncheckcomment_set-1-id").length){
        jQuery("#id_adoptioncheckcomment_set-1-id").parent().hide();
    }
}
window.onload = QAverification;
