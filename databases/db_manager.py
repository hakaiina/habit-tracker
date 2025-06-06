import sqlite3
from datetime import datetime

DB_NAME = 'habits.db'

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Habits (
                Habit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                User_ID INTEGER,
                Name_habit TEXT NOT NULL,
                Description TEXT,
                Target_days INTEGER NOT NULL,
                Create_date TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS HabitProgress (
                Progress_ID INTEGER PRIMARY KEY AUTOINCREMENT,
                Habit_ID INTEGER,
                Date TEXT NOT NULL,
                Completed INTEGER NOT NULL,
                FOREIGN KEY (Habit_ID) REFERENCES Habits(Habit_ID)
            )
        ''')
        # Добавляем таблицу habits_log
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                status TEXT NOT NULL,
                log_date TEXT NOT NULL,
                notes TEXT,
                FOREIGN KEY (habit_id) REFERENCES Habits(Habit_ID)
            )
        ''')
        conn.commit()

def add_habit(user_id, name, desc, target_days):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO Habits (User_ID, Name_habit, Description, Target_days, Create_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, name, desc, target_days, datetime.now().date()))
        conn.commit()

def update_habit(habit_id, name, desc, target_days):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE Habits
            SET Name_habit = ?, Description = ?, Target_days = ?
            WHERE Habit_ID = ?
        ''', (name, desc, target_days, habit_id))
        conn.commit()

def delete_habit(habit_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM Habits WHERE Habit_ID = ?', (habit_id,))
        cursor.execute('DELETE FROM HabitProgress WHERE Habit_ID = ?', (habit_id,))
        cursor.execute('DELETE FROM habits_log WHERE habit_id = ?', (habit_id,))
        conn.commit()

def get_habits_by_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Habits WHERE User_ID = ?', (user_id,))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def add_progress(habit_id, date, completed):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO HabitProgress (Habit_ID, Date, Completed)
            VALUES (?, ?, ?)
        ''', (habit_id, date, completed))
        conn.commit()

def get_progress_by_habit(habit_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT Date, Completed FROM HabitProgress WHERE Habit_ID = ?', (habit_id,))
        return cursor.fetchall()

def get_habit_log_by_date(habit_id, date_str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM habits_log 
            WHERE habit_id = ? AND log_date = ?
        ''', (habit_id, date_str))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

def log_habit_status(habit_id, status, log_date=None, notes=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        log_date = log_date or datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            INSERT INTO habits_log (habit_id, status, log_date, notes)
            VALUES (?, ?, ?, ?)
        ''', (habit_id, status, log_date, notes))
        conn.commit()