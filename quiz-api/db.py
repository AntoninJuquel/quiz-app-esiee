import sqlite3
import os

class QuizDatabase:
    def __init__(self):
        self.db_path = "quiz.db"
        self.db_connection = sqlite3.connect(self.db_path)
        self.db_connection.isolation_level = None

        self.db_init()

    def __del__(self):
        self.db_connection.close()

    def execute_sql(self, query):
        try:
            cur = self.db_connection.cursor()
            cur.execute("begin")

            insertion_result = cur.execute(query)

            cur.execute("commit")

            cur.close()

        except:
            cur.execute("rollback")
            cur.close()
            raise

    def db_init(self):
        self.execute_sql("""
            CREATE TABLE question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            title TEXT,
            image TEXT,
            position INTEGER,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT unique_question UNIQUE (text)
            );

            CREATE TABLE possible_answer (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question_id INTEGER NOT NULL,
            text TEXT NOT NULL,
            isCorrect BOOLEAN NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (question_id) REFERENCES question(id)
            );

        """)

    def rebuild_db(self):
        try:
            os.remove(self.db_path)
        except:
            raise Exception("Could not remove database file")
