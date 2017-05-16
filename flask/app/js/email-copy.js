var $ = require('jquery');

var copyButton = $('#email-copy-button');
var copyText = $('#new-email-success-text');
var copyStatus = $('#copy-status');

$(document).ready( () => {
  copyButton.click( e => {
    copyText.select();
    try {
      var success = document.execCommand('copy');
      if (success) {
        copyStatus.html('Copied!');
      } else {
        copyStatus.html('Unable to copy');
      }
    } catch (err) {
        copyStatus.html('Unable to copy');
    }
  });
});
