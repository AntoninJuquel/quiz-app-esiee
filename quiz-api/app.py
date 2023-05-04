from flask import Flask, request
from models import Question
import jwt_utils
import db

app = Flask(__name__)

@app.route('/')
def hello_world():
	x = 'world'
	return f"Hello, {x}"

@app.route('/quiz-info', methods=['GET'])
def GetQuizInfo():
	return {"size": 0, "scores": []}, 200

@app.route('/login', methods=['POST'])
def Login():
    payload = request.get_json()
    if payload['password'] != 'flask2023':
        return {"error":"Unauthorized"}, 401
    token = jwt_utils.build_token()
    return {"token":token}, 200

@app.route('/rebuild-db', methods=['POST'])
def RebuildDB():
    q_db = db.QuizDatabase()
    q_db.rebuild_db()
    return "Ok", 200

@app.route('/questions', methods=['POST'])
def AddQuestion():
    payload = request.get_json()
    question = Question(None, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'])
    q_db = db.QuizDatabase()
    question_id = q_db.add_question(question.to_dict())
    return {"questionId": question_id}, 200

if __name__ == "__main__":
    app.run()
