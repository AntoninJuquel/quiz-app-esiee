import sqlite3

class QuizDatabase:
    def __init__(self):
        self.db_connection = sqlite3.connect("quiz.db")
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
            CREATE TABLE IF NOT EXISTS Question (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL
            )
        """)
