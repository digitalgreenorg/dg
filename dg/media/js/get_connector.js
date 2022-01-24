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
   $('#recipient-name').css('border', 'solid 3px red');
}
$('.get-connector').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget) // Button that triggered the modal
  var recipient = button.data('whatever') // Extract info from data-* attributes
  // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
  // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
  var modal = $(this)
  modal.find('.modal-body input').val(recipient)
})