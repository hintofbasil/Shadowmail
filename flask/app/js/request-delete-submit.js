const $ = require('jquery');

const clickMeForm = $('#click-me-form');
const clickMeSuccess = $('#click-me-success');
const clickMeError = $('#click-me-error');
const clickMeErrorText = $('#click-me-error-text');
const clickMeUrl = $('#click-me-url');

function processRequest() {
  function getFormData() {
    const data = {};
    const onFormClick = (_, v) => {
      const input = $(v);
      data[input.attr('name')] = input.val();
    };
    $.each(clickMeForm[0].elements, onFormClick);
    // Delete submit button
    delete data.undefined;
    return data;
  }

  function success(response) {
    if (response.status === 'OK') {
      clickMeSuccess.show();
      clickMeError.hide();
    } else {
      clickMeSuccess.hide();
      clickMeError.show();
      clickMeErrorText.html('An expected error occured');
    }
  }

  function error(jqXHR) {
    const json = jqXHR.responseJSON;
    if (json && json.status === 'ERROR' && json.reason) {
      clickMeErrorText.html(json.reason);
    } else {
      clickMeErrorText.html('An expected error occured');
    }
    clickMeSuccess.hide();
    clickMeError.show();
  }

  const json = getFormData();
  $.ajax(
    {
      type: 'POST',
      url: clickMeUrl.html(),
      data: JSON.stringify(json),
      success,
      error,
      contentType: 'application/json',
    },
  );
}

$(document).ready(() => {
  clickMeForm.on('submit', (e) => {
    e.preventDefault();
    processRequest();
  });
});
