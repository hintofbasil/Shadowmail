var request = require('request');

var clickMeForm = document.getElementById('click-me-form');
var clickMeSuccess = document.getElementById('click-me-success');
var clickMeError = document.getElementById('click-me-error');
var clickMeUrl = document.getElementById('click-me-url');

function urlArgsToJson() {
  var url = window.location.href;
  var remove = url.split('?', 1)[0];
  var args = url.substring(remove.length + 1);
  var response = {};
  args.split('&').forEach(function(s) {
    var a = s.split('=');
    response[a[0]] = a[1];
  });
  return response;
}

function processRequest() {
  var json = urlArgsToJson();
  request.post(
    {
      uri: 'http://localhost:5000/api/request_delete',
      json: json
    },

    function(err, response, body) {
      if(body.status == 'OK') {
        clickMeSuccess.style.display = '';
        clickMeError.style.display = 'none';
      } else if (body.status == 'ERROR') {
        clickMeError.innerHTML = 'An error occured:<br />' + body.reason;
        clickMeError.style.display = '';
        clickMeSuccess.style.display = 'none';
      } else {
        clickMeError.innerHTML = 'An unexpected error occured';
        clickMeError.style.display = '';
        clickMeSuccess.style.display = 'none';
      }
    });
}

if (clickMeForm != null) {
  if (clickMeForm.addEventListener) {
    clickMeForm.addEventListener("submit", function(evt) {
      evt.preventDefault();
      processRequest();
    }, true);
  } else {
    clickMeForm.attachEvent('onsubmit', function(evt) {
      evt.preventDefault();
      processRequest();
    });
  }
}
