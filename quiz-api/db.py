import sqlite3
import os

class QuizDatabase:
    def __init__(self):
        self.db_path = os.path.join(os.getcwd(), "quiz.db")
        self.db_connection = sqlite3.connect(self.db_path, check_same_thread=False)
        self.create_tables()

    def __del__(self):
        self.db_connection.close()

    def create_tables(self):
        cursor = self.db_connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                title TEXT NOT NULL,
                image TEXT NOT NULL,
                position INTEGER NOT NULL
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS possible_answers (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                is_correct INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            );
        ''')
        self.db_connection.commit()

    def rebuild_db(self):
        try:
            os.remove(self.db_path)
        except:
            raise Exception("Could not remove database file")
        self.__init__(self.db_path)

    def get_all_questions(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM questions")
        questions = []
        for row in cursor.fetchall():
            question = self.__build_question(row)
            question['possible_answers'] = self.__get_possible_answers(question['id'])
            questions.append(question)
        return questions

    def add_question(self, question):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO questions (text, title, image, position) VALUES (?, ?, ?, ?)", (
            question['text'], question['title'], question['image'], question['position']))
        question_id = cursor.lastrowid
        for answer in question['possible_answers']:
            cursor.execute("INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)", (
                answer['text'], answer['isCorrect'], question_id))
        self.db_connection.commit()
        return question_id

    def update_question(self, question):
        cursor = self.db_connection.cursor()
        cursor.execute("UPDATE questions SET text=?, title=?, image=?, position=? WHERE id=?", (
            question['text'], question['title'], question['image'], question['position'], question['id']))
        cursor.execute("DELETE FROM possible_answers WHERE question_id=?", (question['id'],))
        for answer in question['possible_answers']:
            cursor.execute("INSERT INTO possible_answers (text, is_correct, question_id) VALUES (?, ?, ?)", (
                answer['text'], answer['isCorrect'], question['id']))
        self.db_connection.commit()

    def remove_question(self, question_id):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM questions WHERE id=?", (question_id,))
        cursor.execute("DELETE FROM possible_answers WHERE question_id=?", (question_id,))
        self.db_connection.commit()

    def get_question(self, question_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
        question_row = cursor.fetchone()
        if question_row is None:
            return None
        question = self.__build_question(question_row)
        question['possible_answers'] = self.__get_possible_answers(question_id)
        return question

    def __build_question(self, question_row):
        question = {
            'id': question_row[0],
            'text': question_row[1],
            'title': question_row[2],
            'image': question_row[3],
            'position': question_row[4]
        }
        return question

    def __get_possible_answers(self, question_id):
        cursor = self.db_connection.cursor()
        cursor.execute('SELECT * FROM possible_answers WHERE question_id=?', (question_id,))
        rows = cursor.fetchall()
        answers = []
        for row in rows:
            answer = {
                'id': row[0],
                'text': row[1],
                'is_correct': bool(row[2]),
                'question_id': row[3]
            }
            answers.append(answer)
        return answers


