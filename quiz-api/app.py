from flask import Flask, request
import jwt_utils

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
    return {"token":token}, 200

if __name__ == "__main__":
    app.run()
