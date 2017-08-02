$(function() {
    $("#broadcast_form").submit(function(event) {
        if($("#id_title").val() == 'admin_test') {
            alert("Please select another Meaningful name");
            $("#id_title").val('');
            event.preventDefault();}
    });

    $("#broadcast_test_form").submit(function(event) {
        phone_number = $("#id_to_number").val();
        if(phone_number == '' || phone_number.length < 10 || phone_number.length > 11 || phone_number.match(/[a-z]/i) || parseInt(phone_number) < 7000000000 || parseInt(phone_number) > 9999999999) {
            alert("Please Enter Correct Phone Number.");
            $("#id_to_number").val('');
            event.preventDefault();}
    });
});