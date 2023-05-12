from flask import Flask, request
from question_maker import create_questions
from jwt_utils import is_admin
from models import Question
import datetime
import jwt_utils
import db
import json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    q_db = db.QuizDatabase()
    date = None
    if "date" in request.args:
        date = request.args.get('date')
    questions = q_db.get_all_questions(date)
    score = q_db.get_all_participations(date)
    return {"size": len(questions), "scores": score}, 200

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
    if "date" in payload:
        question = Question(None, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'], payload['date'])
    else:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_date_str = str(current_date)
        question = Question(None, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'], current_date_str)
    q_db = db.QuizDatabase()
    question_id = q_db.add_question(question.to_dict())
    return {"id": question_id}, 200

@app.route('/questions/<int:question_id>', methods=['GET'])
def GetQuestion(question_id):
    q_db = db.QuizDatabase()
    question = q_db.get_question(question_id)
    if question is None:
        return {"error":"Not found"}, 404
    return json.dumps(question), 200

@app.route('/questions/<int:question_id>', methods=['PUT'])
def UpdateQuestion(question_id):
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    payload = request.get_json()
    if "date" in payload:
        question = Question(question_id, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'], payload['date'])
    else:
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_date_str = str(current_date)
        question = Question(question_id, payload['text'], payload['title'], payload['image'], payload['position'], payload['possibleAnswers'], current_date_str)
    q_db = db.QuizDatabase()
    question_exists = q_db.get_question(question_id)
    if question_exists is None:
        return {"error":"Not found"}, 404
    q_db.update_question(question.to_dict())
    return "Ok", 204

@app.route('/questions', methods=['GET'])
def GetQuestionByPosition():
    position = None
    date = None
    if "position" in request.args:
        position = request.args.get('position')
    if "date" in request.args:
        date = request.args.get('date')

    q_db = db.QuizDatabase()

    if position:
        question = q_db.get_question_by_position(position,date)
    else:
        question = q_db.get_all_questions(date)

    if question is None:
        return {"error":"Not found"}, 404
    return json.dumps(question), 200



@app.route('/questions/<int:question_id>', methods=['DELETE'])
def RemoveQuestion(question_id):
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    q_db = db.QuizDatabase()
    question_exists = q_db.get_question(question_id)
    if question_exists is None:
        return {"error":"Not found"}, 404
    q_db.remove_question(question_id)
    return "Ok", 204


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
    q_db = db.QuizDatabase()
    q_db.remove_all_participations()
    return "Ok", 204

@app.route('/create-question-auto', methods=['POST'])
def CreateQuestionAuto():
    if check_auth_header(request.headers.get('Authorization')) is False:
        return {"error":"Unauthorized"}, 401
    q_db = db.QuizDatabase()

    number_of_questions = 3
    date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
    if "number-of-questions" in request.args:
        number_of_questions = int(request.args.get('number-of-questions'))
    if "date" in request.args:
        print("IT WORKKSSS")
        date = str(request.args.get('date'))

    questions = create_questions(number_of_questions)
    for question in questions:
        question['date'] = date
        print(date)
        question['position'] = 1
        q_db.add_question(question)

    text = "Created " + str(len(questions)) + " questions"
    return text, 200

@app.route('/participations', methods=['POST'])
def AddParticipation():
    payload = request.get_json()
    q_db = db.QuizDatabase()
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_date_str = str(current_date)
    questions = q_db.get_all_questions(date=current_date_str)
    difficulty_factor = 1
    if "difficulty" in payload:
        difficulty_factor = payload['difficulty']
    if len(payload['answers']) != len(questions):
        return {"error":"Bad request"}, 400
    
    score = 0
    answsers = payload['answers']
    categories = q_db.get_categories()
    categories_emoji_array = {}
    for category in categories:
        categories_emoji_array[category['name']] = []
    categories_emoji_array['Bonus'] = []
    emoji_txt = ""
    for i in range(len(questions)):
        if answsers[i] < 1:
            if questions[i]['title'] in categories_emoji_array:
                categories_emoji_array[questions[i]['title']].append("❌")
            else:
                categories_emoji_array['Bonus'].append("❌") 
            continue
        if questions[i]['possibleAnswers'][answsers[i] - 1]['isCorrect']:
            if questions[i]['title'] in categories_emoji_array:
                categories_emoji_array[questions[i]['title']].append("✅")
            else:
                categories_emoji_array['Bonus'].append("✅")
            score += 1
        else:
            if questions[i]['title'] in categories_emoji_array:
                categories_emoji_array[questions[i]['title']].append("❌")
            else:
                categories_emoji_array['Bonus'].append("❌") 
    score *= difficulty_factor
    difficulty_emoji = None
    if difficulty_factor == 1:
        difficulty_emoji = "🤓"
    elif difficulty_factor == 2:
        difficulty_emoji = "😎"
    elif difficulty_factor == 3:
        difficulty_emoji = "🤯"
    emoji_txt += "Difficulty: " + difficulty_emoji + "\n"
    for category in categories:
        if len(categories_emoji_array[category['name']]) > 0:
            emoji_txt += category['emoji'] + "".join(categories_emoji_array[category['name']]) + "\n"
    if len(categories_emoji_array['Bonus']) > 0:
        emoji_txt += "🎁" + "".join(categories_emoji_array['Bonus']) + "\n"
    participation_id = q_db.add_score(payload['playerName'], score, difficulty_factor)
    return {"playerName": payload['playerName'], "score":score ,"emoji":emoji_txt}, 200

@app.route('/categories', methods=['GET'])
def GetCategories():
    q_db = db.QuizDatabase()
    categories = q_db.get_categories()
    return json.dumps(categories), 200

if __name__ == "__main__":
    app.run()
