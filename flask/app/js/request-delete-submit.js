var $ = require('jquery');

var clickMeForm = $('#click-me-form');
var clickMeSuccess = $('#click-me-success');
var clickMeError = $('#click-me-error');
var clickMeErrorText = $('#click-me-error-text');
var clickMeUrl = $('#click-me-url');

function processRequest() {

  function getFormData() {
    var data = {}
    $.each(clickMeForm[0].elements, function(i, v) {
      var input = $(v);
      data[input.attr('name')] = input.val();
    });
    // Delete submmit button
    delete data['undefined'];
    return data;
  }

  function success(response, status) {
    if (response.status == 'OK') {
      clickMeSuccess.show();
      clickMeError.hide();
    } else {
      clickMeSuccess.hide();
      clickMeError.show();
      clickMeErrorText.html('An expected error occured')
    }
  };

  function error(jqXHR, status, error) {
    var json = jqXHR.responseJSON;
    if (json && json.status == 'ERROR' && json.reason) {
      clickMeErrorText.html(json.reason);
    } else {
      clickMeErrorText.html('An expected error occured')
    }
    clickMeSuccess.hide();
    clickMeError.show();
  };

  var json = getFormData();
  $.ajax(
    {
      type: 'POST',
      url: clickMeUrl.html(),
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
