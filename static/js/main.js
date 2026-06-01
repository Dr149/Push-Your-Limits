document.addEventListener("DOMContentLoaded", () => {
  const quizContainer = document.getElementById("quiz-container");
  if (!quizContainer) return;

  const quizData = JSON.parse(quizContainer.dataset.quiz || "null");
  if (!quizData) return;

  const state = {
    current: 0,
    correct: 0,
  };

  function renderQuestion() {
    const question = quizData.questions[state.current];
    const card = document.createElement("div");
    card.className = "content-card";
    card.innerHTML = `
      <h3>Question ${state.current + 1}</h3>
      <p>${question.question.replace(/\n/g, "<br />")}</p>
      ${question.image ? `<img src="/uploads/images/${question.image}" alt="Question visual" />` : ""}
      <div class="choices"></div>
    `;

    const choices = card.querySelector(".choices");
    question.choices.forEach((choice) => {
      const button = document.createElement("button");
      button.className = "link-button";
      button.type = "button";
      button.textContent = choice;
      button.addEventListener("click", () => submitAnswer(choice, question.answer));
      choices.appendChild(button);
    });

    quizContainer.innerHTML = "";
    quizContainer.appendChild(card);
  }

  function submitAnswer(selected, answer) {
    const correct = selected === answer;
    if (correct) {
      state.correct += 1;
      flashMessage("Great work! That answer is correct.", "success");
    } else {
      flashMessage(`Nice try — the correct answer is ${answer}.`, "warning");
    }
    state.current += 1;
    if (state.current < quizData.questions.length) {
      setTimeout(renderQuestion, 700);
    } else {
      setTimeout(showResults, 700);
    }
  }

  function showResults() {
    quizContainer.innerHTML = `
      <section class="content-card">
        <h3>Quiz complete</h3>
        <p>You answered <strong>${state.correct}</strong> out of <strong>${quizData.questions.length}</strong> correctly.</p>
        <p>${state.correct === quizData.questions.length ? "Outstanding! Your focus is strong." : "Keep going — every review makes you stronger."}</p>
        <a class="button" href="/">Back to home</a>
      </section>
    `;
  }

  function flashMessage(message, type) {
    const flash = document.createElement("div");
    flash.className = `flash ${type}`;
    flash.textContent = message;
    document.querySelector(".page-shell").prepend(flash);
    setTimeout(() => flash.remove(), 2800);
  }

  renderQuestion();
});
