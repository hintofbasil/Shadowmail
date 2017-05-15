var $ = require('jquery');

$(document).ready( () => {
  var answers = $('.faq-answer');
  var questions = $('.faq-question');
  for (var i = 0; i < questions.length; i++) {
    var answer = $(answers[i]);
    var question = $(questions[i]);
    answer.hide();
    question.click( e => {
      e.preventDefault();
      answer.toggle();
    });
  }
});
