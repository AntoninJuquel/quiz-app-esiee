import sqlite3
import datetime
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
                position INTEGER NOT NULL,
                date TEXT DEFAULT (strftime('%Y-%m-%d','now'))
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS possible_answers (
                id INTEGER PRIMARY KEY,
                text TEXT NOT NULL,
                isCorrect INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                FOREIGN KEY (question_id) REFERENCES questions (id)
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS participations (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                score INTEGER NOT NULL,
                difficulty INTEGER NOT NULL DEFAULT 1,
                date TEXT DEFAULT (strftime('%Y-%m-%d','now'))
            );
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS questions_category (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                emoji TEXT NOT NULL
            )
        ''')
        self.db_connection.commit()

        # insert default categories
        cursor.execute("SELECT * FROM questions_category")
        if len(cursor.fetchall()) == 0:
            cursor.execute("INSERT INTO questions_category (name, emoji) VALUES (?, ?)", ("Géographie", "🌍"))
            cursor.execute("INSERT INTO questions_category (name, emoji) VALUES (?, ?)", ("Histoire", "📜"))
            cursor.execute("INSERT INTO questions_category (name, emoji) VALUES (?, ?)", ("Culture Générale", "📚"))
            cursor.execute("INSERT INTO questions_category (name, emoji) VALUES (?, ?)", ("Musique", "🎵"))
            cursor.execute("INSERT INTO questions_category (name, emoji) VALUES (?, ?)", ("Science", "🔬"))
        
        self.db_connection.commit()


    def rebuild_db(self):
        try:
            os.remove(self.db_path)
        except:
            raise Exception("Could not remove database file")
        self.__init__()

    def get_all_questions(self,date=None):
        cursor = self.db_connection.cursor()
        if date:
            cursor.execute("SELECT * FROM questions WHERE date=? ORDER BY position ASC", (date,))
        else:
            cursor.execute("SELECT * FROM questions ORDER BY position ASC")
        questions = []
        for row in cursor.fetchall():
            question = self.__build_question(row)
            question['possibleAnswers'] = self.__get_possible_answers(question['id'])
            questions.append(question)
        return questions

    def add_question(self, question):
        cursor = self.db_connection.cursor()

        date = question['date']
        if date:
            cursor.execute("SELECT id FROM questions WHERE position=? AND date=?", (question['position'], date))
        else:
            cursor.execute("SELECT id FROM questions WHERE position=?", (question['position'],))
        row = cursor.fetchone()
        if row is not None:
            question_id = row[0]
            self.shift_position_up(question_id, date)

        if "date" in question:
            cursor.execute("INSERT INTO questions (text, title, image, position, date) VALUES (?, ?, ?, ?, ?)", (
                question['text'], question['title'], question['image'], question['position'], question['date']))
        else:
            cursor.execute("INSERT INTO questions (text, title, image, position) VALUES (?, ?, ?, ?)", (
                question['text'], question['title'], question['image'], question['position']))
        question_id = cursor.lastrowid
        for answer in question['possibleAnswers']:
            cursor.execute("INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)", (
                answer['text'], answer['isCorrect'], question_id))
        self.db_connection.commit()
        return question_id

    def shift_position_down(self, question_id, date):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT position FROM questions WHERE id=?", (question_id,))
        row = cursor.fetchone()
        position = row[0]
        next_question_id = None
        cursor.execute("SELECT id FROM questions WHERE position=?", (position + 1,))
        row = cursor.fetchone()
        if row is not None:
            next_question_id = row[0]
        cursor.execute("UPDATE questions SET position=? WHERE id=?", (position - 1, question_id))
        self.db_connection.commit()
        if next_question_id is not None:
            self.shift_position_down(next_question_id, date)

    def shift_position_up(self, question_id, date):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT position FROM questions WHERE id=?", (question_id,))
        row = cursor.fetchone()
        position = row[0]
        next_question_id = None
        cursor.execute("SELECT id FROM questions WHERE position=?", (position + 1,))
        row = cursor.fetchone()
        if row is not None:
            next_question_id = row[0]
        cursor.execute("UPDATE questions SET position=? WHERE id=?", (position + 1, question_id))
        self.db_connection.commit()
        if next_question_id is not None:
            self.shift_position_up(next_question_id, date)

    def update_question(self, question):
        cursor = self.db_connection.cursor()

        question_id = question['id']
        date = question['date']
        new_pos = question['position']
        old_pos = None
        cursor.execute("SELECT position FROM questions WHERE id=?", (question['id'],))
        row = cursor.fetchone()
        if row is not None:
            old_pos = row[0]

        questions = self.get_all_questions(date=date)
        if len(questions) > 0:
            q_arr = []
            for q in questions:
                q_arr.append({q["id"]: q["position"]})

            my_q = q_arr.pop(old_pos - 1)
            q_arr.insert(new_pos - 1, my_q)
            
            def update_pos(q_id, pos):
                cursor.execute("UPDATE questions SET position=? WHERE id=?", (pos, q_id))
                self.db_connection.commit()

            for i, q in enumerate(q_arr):
                q_id = list(q.keys())[0]
                pos = i + 1
                update_pos(q_id, pos)

        if "date" in question:
            cursor.execute("UPDATE questions SET text=?, title=?, image=?, position=? WHERE id=?", (
                question['text'], question['title'], question['image'], question['position'], question['id']))
        else:
            cursor.execute("UPDATE questions SET text=?, title=?, image=?, position=? date=? WHERE id=?", (
                question['text'], question['title'], question['image'], question['position'], question['date'], question['id']))
        cursor.execute("DELETE FROM possible_answers WHERE question_id=?", (question['id'],))
        for answer in question['possibleAnswers']:
            cursor.execute("INSERT INTO possible_answers (text, isCorrect, question_id) VALUES (?, ?, ?)", (
                answer['text'], answer['isCorrect'], question['id']))
        self.db_connection.commit()

    def remove_question(self, question_id):
        cursor = self.db_connection.cursor()
        position = None
        date = None
        cursor.execute("SELECT date FROM questions WHERE id=?", (question_id,))
        row = cursor.fetchone()
        if row is not None:
            date = row[0]
        cursor.execute("SELECT position FROM questions WHERE id=?", (question_id,))
        row = cursor.fetchone()
        if row is not None:
            position = row[0]
        if position is not None:
            next_question_id = None
            cursor.execute("SELECT id FROM questions WHERE position=?", (position + 1,))
            row = cursor.fetchone()
            if row is not None:
                next_question_id = row[0]
        cursor.execute("DELETE FROM questions WHERE id=?", (question_id,))
        cursor.execute("DELETE FROM possible_answers WHERE question_id=?", (question_id,))
        self.db_connection.commit()
        if next_question_id is not None:
            self.shift_position_down(next_question_id, date)
    
    def remove_all_questions(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM questions")
        cursor.execute("DELETE FROM possible_answers")
        self.db_connection.commit()

    def get_question(self, question_id):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM questions WHERE id=?", (question_id,))
        question_row = cursor.fetchone()
        if question_row is None:
            return None
        question = self.__build_question(question_row)
        question['possibleAnswers'] = self.__get_possible_answers(question_id)
        return question
    
    def get_question_by_position(self, position, date=None):
        cursor = self.db_connection.cursor()
        if date is not None:
            cursor.execute("SELECT * FROM questions WHERE position=? AND date=?", (position, date))
        else:
            cursor.execute("SELECT * FROM questions WHERE position=?", (position,))
        question_row = cursor.fetchone()
        if question_row is None:
            return None
        question = self.__build_question(question_row)
        question['possibleAnswers'] = self.__get_possible_answers(question['id'])
        return question

    def __build_question(self, question_row):
        question = {
            'id': question_row[0],
            'text': question_row[1],
            'title': question_row[2],
            'image': question_row[3],
            'position': question_row[4],
            'date' : question_row[5]
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
                'isCorrect': bool(row[2]),
                'question_id': row[3]
            }
            answers.append(answer)
        return answers

    def get_all_participations(self, date=None):
        cursor = self.db_connection.cursor()
        if date:
            cursor.execute("SELECT * FROM participations WHERE date=? ORDER BY score DESC", (date,))
        else:
            cursor.execute("SELECT * FROM participations ORDER BY score DESC")
        rows = cursor.fetchall()
        participations = []
        for row in rows:
            participation = {
                'playerName': row[1],
                'score': row[2],
                'difficulty': row[3],
                'date' : row[4]
            }
            participations.append(participation)
        return participations

    def add_score(self, player_name, score, difficulty):
        cursor = self.db_connection.cursor()
        cursor.execute("INSERT INTO participations (name, score, difficulty) VALUES (?, ?, ?)", (player_name, score, difficulty))
        self.db_connection.commit()


    def remove_all_participations(self):
        cursor = self.db_connection.cursor()
        cursor.execute("DELETE FROM participations")
        self.db_connection.commit()

    def get_categories(self):
        cursor = self.db_connection.cursor()
        cursor.execute("SELECT * FROM questions_category")
        rows = cursor.fetchall()
        categories = []
        for row in rows:
            category = {
                'id': row[0],
                'name': row[1],
                'emoji' : row[2]
            }
            categories.append(category)
        return categories
