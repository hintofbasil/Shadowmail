const $ = require('jquery');
const cookies = require('js-cookie');

const newEmailForm = $('#new-email-form');
const newEmailSuccess = $('#new-email-success');
const newEmailSuccessText = $('#new-email-success-text');
const newEmailError = $('#new-email-error');
const newEmailErrorText = $('#new-email-error-text');
const newEmailInput = $('#new-email-input');

function requestNewEmail() {
  function success(response) {
    if (response.status === 'OK') {
      newEmailSuccessText.val(response.email);
      newEmailError.hide();
      newEmailSuccess.show();

      // Set cookie and clear input
      cookies.set('previous-email', newEmailInput.val());
      newEmailInput.val('');
    } else {
      newEmailErrorText.html('An unexpected error occured');
      newEmailError.show();
      newEmailSuccess.hide();
    }
  }

  const error = (jqXHR) => {
    const json = jqXHR.responseJSON;
    if (json && json.status === 'ERROR' && json.reason) {
      newEmailErrorText.html(json.reason);
    } else {
      newEmailErrorText.html('An unexpected error occured');
    }
    newEmailError.show();
    newEmailSuccess.hide();
  };

  const email = newEmailInput.val();
  const data = JSON.stringify({ email });
  $.ajax(
    {
      type: 'POST',
      url: '/api/new',
      data,
      success,
      error,
      contentType: 'application/json',
    },
  );
}

$(document).ready(() => {
  newEmailForm.on('submit', (e) => {
    e.preventDefault();
    requestNewEmail();
  });
  const emailCookie = cookies.get('previous-email');
  if (emailCookie) {
    newEmailInput.val(emailCookie);
  }
});
