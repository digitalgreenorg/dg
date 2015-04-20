/**
 * Created by Lokesh on 2015-03-17.
 */

function QAverification() {
    jQuery("#id_verification_status").change(function () {
        if (jQuery("#id_verification_status").val() != 0) {
            jQuery("#id_adoptioncheckcomment_set-0-comment_msg").prop('disabled', false);
        }
        if (jQuery("#id_verification_status").val() == 0) {
            jQuery("#id_adoptioncheckcomment_set-0-comment_msg").val("");
            jQuery("#id_adoptioncheckcomment_set-0-comment_msg").prop('disabled', true);
        }
    });

    if (jQuery("#id_verification_status option:selected").val() == 0) {
        jQuery('#id_adoptioncheckcomment_set-0-comment_msg').prop('disabled', true);
    }
}
window.onload = QAverification;
