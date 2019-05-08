const $ = require('jquery');

const copyButton = $('#email-copy-button');
const copyText = $('#new-email-success-text');
const copyStatus = $('#copy-status');

$(document).ready(() => {
  copyButton.click(() => {
    copyText.select();
    try {
      const success = document.execCommand('copy');
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
