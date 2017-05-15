var $ = require('jquery');

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

$(document).ready( () => {
  var args = urlArgsToJson();
  var emailContainer = $('.request-delete-email');
  if (emailContainer) {
    if (args && args.email) {
      emailContainer.html(args.email);
    } else {
      emailContainer.html('No email specified');
    }
  }
});
