import requests

class UnitTests:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
    
    def print_success(self, test_name):
        print("\033[92m" + test_name + " passed\033[0m")
    
    def print_error(self, test_name):
        print("\033[91m" + test_name + " failed\033[0m")

    def get_token(self):
        url = self.base_url + "/login"
        response = requests.post(url, json={"password":"flask2023"})
        return response.json()['token']

    def create_question(self, question_dict):
        res = requests.post(self.base_url + "/questions", json=question_dict, headers={"Authorization": "Bearer " + self.get_token()})

    def tearup(self):
        url = self.base_url + "/rebuild-db"
        response = requests.post(url, json={"password":"flask2023"})

class TestUpdateQuestions(UnitTests):
    def __init__(self):
        super().__init__()
        question_dict = {
            "text": "What is the capital of France?",
            "title": "Geography",
            "image": "https://www.google.com/url?sa=i&url=https%3A%2F%2Fwww.123rf.com%2Fphoto_14357497_paris-eiffel-tower-capital-of-france.html&psig=AOvVaw0z9p5l5Z5Y5Z5Y5Z5Y5Z5Y&ust=1619926706167000&source=images&cd=vfe&ved=0CAIQjRxqFwoTCJjBx7eH0PACFQAAAAAdAAAAABAD",
            "position": 1,
            "possibleAnswers": [{"text": "Paris", "isCorrect": True}, {"text": "London", "isCorrect": False}, {"text": "Berlin", "isCorrect": False}, {"text": "Madrid", "isCorrect": False}],
            "date": "2021-05-01"
        }
        self.create_question(question_dict)
        self.create_question(question_dict)
        self.create_question(question_dict)
        self.create_question(question_dict)

    def test_read_questions(self):
        url = self.base_url + "/quiz-info?date=2021-05-01"
        response = requests.get(url)
        if response.status_code != 200:
            self.print_error("test_read_questions has wrong status code")
            return
        data = response.json()
        if data['size'] != 4:
            self.print_error("test_read_questions has wrong size")
            return
        self.print_success("test_read_questions passed")

if __name__ == "__main__":
    # lauch every class that inherits from UnitTests, and run all methods that start with "test_"
    # tearup 
    UnitTests().tearup()
    for cls in UnitTests.__subclasses__():
        for name in dir(cls):
            if name.startswith("test_"):
                getattr(cls(), name)()
    UnitTests().tearup()