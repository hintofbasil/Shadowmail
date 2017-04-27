var request = require('request');

var newEmailForm = document.getElementById('new-email-form');
var newEmailSuccess = document.getElementById('new-email-success');
var newEmailError = document.getElementById('new-email-error');
var newEmailInput = document.getElementById('new-email-input');

function requestNewEmail() {
  var email = newEmailInput.value;
  request.post(
    {
      uri: 'http://localhost:5000/new',
      json: {email: email}
    },

    function(err, response, body) {
      if(body.status == 'OK') {
        newEmailSuccess.innerHTML = body.email;
      } else if (body.status == 'ERROR') {
        newEmailError.innerHTML = 'An error occured:<br />' + body.reason;
      } else {
        newEmailError.innerHTML = 'An unexpected error occured';
      }
    });
}

if (newEmailForm.addEventListener) {
  newEmailForm.addEventListener("submit", function(evt) {
    evt.preventDefault();
    requestNewEmail();
  }, true);
} else {
  newEmailForm.attachEvent('onsubmit', function(evt) {
    evt.preventDefault();
    requestNewEmail();
  });
}
