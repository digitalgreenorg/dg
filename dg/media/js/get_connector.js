function getConnector() {
  var filter = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
  let email = $('#recipient-name').attr('value')
    if (filter.test(email))  {
            url = window.location.href
            url = url+ '/get_data?email=' + email;
            $.get(url, function(data, status){
                window.location = data['data']

    });
   }
   else {
        $('#recipient-name').css('border', 'solid 3px red');
   }
}
$('.get-connector').on('show.bs.modal', function (event) {
  var modal = $(this)
  modal.find('.modal-body input').val(recipient)
})