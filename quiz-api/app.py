from flask import Flask, request
from jwt_utils import is_admin
from models import Question
import jwt_utils
import db
import json

app = Flask(__name__)

def check_auth_header(auth_header):
    if auth_header is None:
        return False
    token = auth_header.split(' ')[1]
    return is_admin(token)

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
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    payload = request.get_json()
    question = Question(None, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'])
    q_db = db.QuizDatabase()
    question_id = q_db.add_question(question.to_dict())
    return {"id": question_id}, 200

@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestion(question_id):
    q_db = db.QuizDatabase()
    question = q_db.get_question(question_id)
    if question is None:
        return {"error":"Not found"}, 404
    print("dumps : ", json.dumps(question))
    return json.dumps(question), 200

@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
    position = request.args.get('position')
    q_db = db.QuizDatabase()
    question = q_db.get_question_by_position(position)
    if question is None:
        return {"error":"Not found"}, 404
    return json.dumps(question), 200



@app.route('/questions/<int:question_id>', methods=['DELETE'])
def RemoveQuestion(question_id):
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    q_db = db.QuizDatabase()
    q_db.remove_question(question_id)
    return "Ok", 200


@app.route('/questions/all', methods=['DELETE'])
def RemoveAllQuestions():
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    q_db = db.QuizDatabase()
    q_db.remove_all_questions()
    return "Ok", 204

@app.route('/participations/all', methods=['DELETE'])
def RemoveAllParticipations():
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    return "Ok", 204

if __name__ == "__main__":
    app.run()
