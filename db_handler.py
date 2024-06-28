import random
import sqlite3
import random

class CatDB:
    def __init__(self, db_name='cat_ai.db'):
        self.db_name = db_name
        self.initialize_db()

    def initialize_db(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS questions
                          (id INTEGER PRIMARY KEY, question TEXT UNIQUE)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS answers
                          (id INTEGER PRIMARY KEY, answer TEXT, question_id INTEGER,
                          FOREIGN KEY(question_id) REFERENCES questions(id))''')
        conn.commit()
        conn.close()

    def insert_question_answer(self, question, answer):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('SELECT id FROM questions WHERE question = ?', (question,))
        question_id = cursor.fetchone()
        
        if question_id:
            question_id = question_id[0]
        else:
            cursor.execute('INSERT INTO questions (question) VALUES (?)', (question,))
            question_id = cursor.lastrowid
        
        cursor.execute('INSERT INTO answers (answer, question_id) VALUES (?, ?)', (answer, question_id))
        
        conn.commit()
        conn.close()

    def get_answers(self, question):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT answers.answer FROM answers
                          JOIN questions ON questions.id = answers.question_id
                          WHERE questions.question = ?''', (question,))
        
        answers = cursor.fetchall()
        conn.close()
        
        if answers:
            return random.choice([answer[0] for answer in answers])
        else:
            return None
        
    def get_all_questions_answers(self):
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        
        cursor.execute('''SELECT questions.question, answers.answer FROM questions
                          JOIN answers ON questions.id = answers.question_id''')
        
        questions_answers = cursor.fetchall()
        conn.close()
        
        return questions_answers