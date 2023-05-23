import requests
from db import QuizDatabase
import sys

class UnitTests:
    def __init__(self):
        self.base_url = "http://127.0.0.1:5000"
        self.current_date = "2021-05-01"
        self.tomorrow_date = "2021-05-02"
    
    def print_success(self, test_name):
        success_emoji = "✅"
        print("\033[92m" + success_emoji + " " +  test_name + " \033[0m")
    
    def print_error(self, test_name):
        error_emoji = "❌"
        # get the line where error occured
        import inspect
        line_num = inspect.currentframe().f_back.f_lineno
        print("\033[91m" + error_emoji + " " +  test_name + " \033[0m" + " at line " + str(line_num))

    def get_token(self):
        url = self.base_url + "/login"
        response = requests.post(url, json={"password":"flask2023"})
        return response.json()['token']

    def create_question(self, question_dict):
        res = requests.post(self.base_url + "/questions", json=question_dict, headers={"Authorization": "Bearer " + self.get_token()})

    def tearup(self):
        url = self.base_url + "/rebuild-db"
        response = requests.post(url, json={"password":"flask2023"})

class TestReadQuestions(UnitTests):
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
        self.print_success("test_read_questions 4 questions were created") 
        self.tearup()

class TestCreateQuestionAuto(UnitTests):
    def __init__(self):
        super().__init__()
        self.number_of_questions = 2
        self.number_of_supported_categories = 3
        self.current_cats = ["Géographie", "Histoire", "Musique"]
        self.test_create_question_auto_endpoint = self.base_url + "/create-question-auto?number-of-questions=" + str(self.number_of_questions) + "&date=" + self.current_date
    
    def test_create_question_auto(self):
        token = self.get_token()
        res = requests.post(self.test_create_question_auto_endpoint, headers={"Authorization": "Bearer " + token})
        if res.status_code == 200:
            self.print_success("test_create_question_auto passed")
        else:
            self.print_error("test_create_question_auto failed")



    def test_read_questions_auto(self):
        # get all questions at current date
        url = self.base_url + "/quiz-info?date=" + self.current_date
        response = requests.get(url)
        res = response.json()
        if res['size'] == self.number_of_questions * self.number_of_supported_categories:
            self.print_success("test_read_questions_auto passed")
        else:
            self.print_error("test_read_questions_auto failed")

        url = self.base_url + "/questions?date=" + self.current_date
        response = requests.get(url)
        res = response.json()

        tmp_cat_list = self.current_cats.copy()
        for question in res:
            if question['title'] in tmp_cat_list:
                tmp_cat_list.remove(question['title'])
        
        if len(tmp_cat_list) == 0:
            self.print_success("test_read_questions_auto passed")
        else:
            self.print_error("test_read_questions_auto failed")

    def test_update_auto_question(self):
        # list all questions
        url = self.base_url + "/questions" 
        response = requests.get(url)
        questions = response.json()
        questions_dict = []
        for question in questions:
            data = {
                "id": question['id'],
                "position": question['position'],
                "title": question['title']
            }
            questions_dict.append(data)
        
        num = self.number_of_questions * self.number_of_supported_categories

        def update_question_to_tomorrow(id):
            # get question as json
            url = self.base_url + "/questions/" + str(id)
            response = requests.get(url)
            question = response.json()
            # update question
            question['date'] = self.tomorrow_date
            # send put request
            url = self.base_url + "/questions/" + str(id)
            response = requests.put(url, json=question, headers={"Authorization": "Bearer " + self.get_token()})
            if response.status_code == 204:
                self.print_success("question updated successfully")
            else:
                self.print_error("question not updated successfully")

        def check_positions_are_valid(date):
            # get all questions at current date
            # check that positions are valid, starts at 1 and just increments by 1
            url = self.base_url + "/questions?date=" + date
            response = requests.get(url)
            res = response.json()
            for i in range(len(res)):
                if res[i]['position'] != i + 1:
                    self.print_error("positions are not valid")
                    return
                else:
                    self.print_success("positions are valid")
            

        # get num from quiz info
        num = requests.get(self.base_url + "/quiz-info?date=" + self.current_date).json()['size']
        for position in range(int(num/2) ,num ):
            update_question_to_tomorrow(questions_dict[position]['id'])
            check_positions_are_valid(self.current_date)
            check_positions_are_valid(self.tomorrow_date)

class TestCrudCategory(UnitTests):
    def __init__(self):
        super().__init__()
        self.test_category_endpoint = self.base_url + "/categories"
        self.test_category = {
            "name": "Cinéma",
            "emoji": "🎬"
        }

    def test_create_category(self):
        res = requests.post(self.test_category_endpoint, json=self.test_category, headers={"Authorization": "Bearer " + self.get_token()})
        if res.status_code == 201:
            self.print_success("test_create_category passed")
        else:
            self.print_error("test_create_category failed")

    def test_read_category(self):
        res = requests.get(self.test_category_endpoint)
        if res.status_code == 200:
            self.print_success("test_read_category passed")
        else:
            self.print_error("test_read_category failed")

        # check cinema category is in the list
        res = res.json()
        isInList = False
        for category in res:
            if category['name'] == self.test_category['name']:
                isInList = True
        if isInList:
            self.print_success("test_read_category passed")
        else:
            self.print_error("test_read_category failed")
    
    def test_update_category(self):
        # get all categories
        res = requests.get(self.test_category_endpoint)
        res = res.json()
        for category in res:
            if category['name'] == self.test_category['name']:
                category['name'] = "Cinéma 2"
                category['emoji'] = "🎥"
                # update category
                res = requests.put(self.test_category_endpoint + "/" + str(category['id']), json=category, headers={"Authorization": "Bearer " + self.get_token()})
                if res.status_code == 204:
                    self.print_success("test_update_category passed")
                else:
                    self.print_error("test_update_category failed")
                return
        self.print_error("test_update_category failed")

    def test_delete_questions_from_date_tomorrow(self):
        delete_endpoint = self.base_url + "/questions/all?date=" + self.tomorrow_date
        res = requests.delete(delete_endpoint, headers={"Authorization": "Bearer " + self.get_token()})
        if res.status_code == 204:
            self.print_success("test_delete_questions_from_date_tomorrow passed")
        else:
            self.print_error("test_delete_questions_from_date_tomorrow failed")
        
        # check todays questions are still there
        res = requests.get(self.base_url + "/questions?date=" + self.current_date)
        res = res.json()
        if len(res) != 0:
            self.print_success("test_delete_questions_from_date_tomorrow passed")
        else:
            self.print_error("test_delete_questions_from_date_tomorrow failed")


    def test_delete_category(self):
        # get all categories
        res = requests.get(self.test_category_endpoint)
        res = res.json()
        for category in res:
            if category['name'] == "Cinéma 2":
                # delete category
                res = requests.delete(self.test_category_endpoint + "/" + str(category['id']), headers={"Authorization": "Bearer " + self.get_token()})
                if res.status_code == 204:
                    self.print_success("test_delete_category passed")

    def test_generate_and_delete(self):
        self.test_create_question_auto_endpoint = self.base_url + "/create-question-auto?number-of-questions=3"
        token = self.get_token()
        for i in range(3):
            res = requests.post(self.test_create_question_auto_endpoint, headers={"Authorization": "Bearer " + token})
            if res.status_code == 200:
                self.print_success("test_create_question_auto passed " + str(i + 1) + "/3")
            else:
                self.print_error("test_create_question_auto failed")
        

if __name__ == "__main__":
    # lauch every class that inherits from UnitTests, and run all methods that start with "test_"
    # tearup 
    UnitTests().tearup()
    for cls in UnitTests.__subclasses__():
        for name in dir(cls):
            if name.startswith("test_"):
                getattr(cls(), name)()