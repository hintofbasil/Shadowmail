var $ = require('jquery');

var newEmailForm = $('#new-email-form');
var newEmailSuccess = $('#new-email-success');
var newEmailError = $('#new-email-error');
var newEmailInput = $('#new-email-input');

function requestNewEmail() {

  function success(response, status) {
    if(response.status == 'OK') {
      newEmailSuccess.html(response.email);
      newEmailError.hide();
      newEmailSuccess.show();
    } else {
      newEmailError.html('An unexpected error occured');
      newEmailError.show();
      newEmailSuccess.hide();
    }
  };

  function error(jqXHR, status, error) {
    var json = jqXHR.responseJSON
    if (json && json.status == 'ERROR' && json.reason) {
      newEmailError.html('An error occured:<br />' + jqXHR.responseJSON.reason);
    } else {
      newEmailError.html('An unexpected error occured');
    }
    newEmailError.show();
    newEmailSuccess.hide();
  };

  var email = newEmailInput.val();
  var data = JSON.stringify({email: email});
  $.ajax(
    {
      type: 'POST',
      url: 'http://localhost:5000/api/new',
      data: data,
      success: success,
      error: error,
      contentType: "application/json"
    }
  );

}

$(document).ready( () => {
  newEmailForm.on('submit', e => {
    e.preventDefault();
    requestNewEmail();
  });
});
