var $ = require('jquery');

var clickMeForm = $('#click-me-form');
var clickMeSuccess = $('#click-me-success');
var clickMeError = $('#click-me-error');
var clickMeUrl = $('#click-me-url');

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

  function success(response, status) {
    if (response.status == 'OK') {
      clickMeSuccess.show();
      clickMeError.hide();
    } else {
      clickMeSuccess.hide();
      clickMeError.show();
      clickMeError.html('An expected error occured')
    }
  };

  function error(jqXHR, status, error) {
    var json = jqXHR.responseJSON;
    if (json && json.status == 'ERROR' && json.reason) {
      clickMeError.html('An error occured:<br />' + json.reason);
    } else {
      clickMeError.html('An expected error occured')
    }
    clickMeSuccess.hide();
    clickMeError.show();
  };

  var json = urlArgsToJson();
  $.ajax(
    {
      type: 'POST',
      url: 'http://localhost:5000/api/request_delete',
      data: JSON.stringify(json),
      success: success,
      error: error,
      contentType: "application/json"
    }
  );
}

$(document).ready( () => {
  clickMeForm.on('submit', e => {
    e.preventDefault();
    processRequest();
  });
});
