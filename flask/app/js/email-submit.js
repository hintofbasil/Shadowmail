var request = require('request');

var newEmailForm = document.getElementById('new-email-form');

function requestNewEmail() {
  request.post(
    {
      uri: 'http://localhost:5000/new',
      json: {email:'test@example.com'}
    },

    function(err, response, body) {
      if(body.status == 'OK') {
        console.log('New email: ' + body.email);
      } else if (body.status == 'ERROR') {
        console.log('An error occured' + body.reason);
      } else {
        console.log('An unexpected error occured');
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
