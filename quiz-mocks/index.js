const express = require("express");

const app = express();

app.use(express.json());

app.get("/", (req, res) => {
  res.send("Hello World!");
});

app.post("/answers", (req, res) => {
  const { answers } = req.body;
  const correctAnswers = [[0, 3], [1, 2], [0, 3], [1]];
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
