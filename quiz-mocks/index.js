const express = require("express");
const cors = require("cors");

const db = require("./db");

const app = express();

app.use(express.json());
app.use(cors());

app.get("/", (req, res) => {
  res.send("Hello World!");

  console.log(db);
});

app.get("/questions", (req, res) => {
  const { position } = req.query;
  const question = db.questions[position];
  res.json(question);
});

app.get("/quiz-info", (req, res) => {
  res.json(db["quiz-info"]);
});

app.post("/participations", (req, res) => {
  const { answers, playerName } = req.body;
  console.log(answers, playerName);
  const correctAnswers = db.questions.map((question) => {
    const possibleAnswers = question.possibleAnswers;
    const correctIndices = [];
    possibleAnswers.forEach((answer, index) => {
      if (answer.isCorrect) {
        correctIndices.push(index);
      }
    });
    return correctIndices;
  });
  console.log(correctAnswers);
  let score = 0;
  correctAnswers.forEach((correctAnswer, index) => {
    const answer = answers[index];
    if (Array.isArray(answer)) {
      answer.forEach((a) => {
        if (correctAnswer.includes(a)) {
          score++;
        } else {
          score--;
        }
      });
    } else {
      if (correctAnswer.includes(answer)) {
        score++;
      } else {
        score--;
      }
    }
  });
  res.json({ score });
});

app.listen(5000, () => {
  console.log("Listening on port 5000");
});
