from flask import Flask, request
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
    token = jwt_utils.build_token()
    q_db = db.QuizDatabase()
    q_db.execute_sql("INSERT INTO Question (title) VALUES ('What is the capital of France?');")
    return {"token":token}, 200

#Récupérer le token envoyé en paramètre
#request.headers.get('Authorization')

#récupèrer un l'objet json envoyé dans le body de la requète
#request.get_json()

if __name__ == "__main__":
    app.run()
