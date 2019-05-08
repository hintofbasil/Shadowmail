const $ = require('jquery');

$(document).ready(() => {
  const answers = $('.faq-answer');
  const questions = $('.faq-question');
  for (let i = 0; i < questions.length; i += 1) {
    const answer = $(answers[i]);
    const question = $(questions[i]);
    answer.hide();
    question.click((e) => {
      $(e.currentTarget.nextElementSibling).toggle();
      e.preventDefault();
    });
  }
});
