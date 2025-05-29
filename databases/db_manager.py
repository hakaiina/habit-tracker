import sqlite3
from datetime import datetime

DB_NAME = "habit_tracker.db"


def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Username TEXT NOT NULL,
            Reg_date TEXT DEFAULT CURRENT_DATE
            )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habits (
            Habit_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            User_ID INTEGER,
            Name_habit TEXT NOT NULL,
            Description TEXT,
            Target_days INTEGER,
            Create_days TEXT DEFAULT CURRENT_DATE,
            FOREIGN KEY (User_ID) REFERENCES Users(User_ID)
            )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Reminder (
            Reminder_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Habit_ID INTEGER,
            Time TEXT,
            Days TEXT,
            FOREIGN KEY (Habit_ID) REFERENCES Habits(Habit_ID)
            )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Status (
            Status_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Name_status TEXT NOT NULL
            )""")

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Habits_log (
            Log_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Habit_ID INTEGER,
            Status_ID INTEGER,
            Date_start TEXT,
            Date_end TEXT,
            Notes TEXT,
            FOREIGN KEY (Habit_ID) REFERENCES Habits(Habit_ID),
            FOREIGN KEY (Status_ID) REFERENCES Status(Status_ID)
            )""")

        cursor.execute("INSERT OR IGNORE INTO Status (Status_ID, Name_status) VALUES (1, 'Done'), (2, 'Skipped')")


def add_user(username):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (Username) VALUES (?)", (username,))
        conn.commit()
        return cursor.lastrowid


def add_habit(user_id, name, desc, target_days):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Habits (User_ID, Name_habit, Description, Target_days)
            VALUES (?, ?, ?, ?)
            """, (user_id, name, desc, target_days))
        conn.commit()
        return cursor.lastrowid


def get_all_habits(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Habits WHERE User_ID = ?", (user_id,))
        return cursor.fetchall()


def add_habit_log(habit_id, status_id, date_start=None, date_end=None, notes=""):
    if date_start is None:
        date_start = datetime.now().date().isoformat()

    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Habits_log (Habit_ID, Status_ID, Date_start, Date_end, Notes)
            VALUES (?, ?, ?, ?, ?)
            """, (habit_id, status_id, date_start, date_end, notes))
        conn.commit()
        return cursor.lastrowid

def update_habit(habit_id, name, desc, target_days):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Habits
            SET Name_habit = ?, Description = ?, Target_days = ?
            WHERE Habit_ID = ?
        """, (name, desc, target_days, habit_id))
        conn.commit()


def get_logs_by_habit(habit_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT HL.Log_ID, HL.Date_start, HL.Date_end, HL.Notes, S.Name_status
            FROM Habits_log HL
            JOIN Status S ON HL.Status_ID = S.Status_ID
            WHERE HL.Habit_ID = ?
            ORDER BY HL.Date_start DESC
        """, (habit_id,))
        return cursor.fetchall()


def get_habit_logs_by_user(user_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h1.Date_start, s.Name_status
            FROM Habits_log h1
            JOIN Habits h ON h.Habit_ID = h1.Habit_ID
            JOIN Status s ON h1.Status_ID = s.Status_ID
            WHERE h.User_ID = ?
        """, (user_id,))
        return cursor.fetchall()


def get_logs_by_date(user_id, date_str):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT H.Name_habit, HL.Date_start, S.Name_status
            FROM Habits_log HL
            JOIN Habits H ON HL.Habit_ID = H.Habit_ID
            JOIN Status S ON HL.Status_ID = S.Status_ID
            WHERE H.User_ID = ? AND HL.Date_start = ?
        """, (user_id, date_str))
        return cursor.fetchall()


def update_habit_log(log_id, status_id=None, date_start=None, date_end=None, notes=None):
    fields = []
    params = []

    if status_id is not None:
        fields.append("Status_ID = ?")
        params.append(status_id)
    if date_start is not None:
        fields.append("Date_start = ?")
        params.append(date_start)
    if date_end is not None:
        fields.append("Date_end = ?")
        params.append(date_end)
    if notes is not None:
        fields.append("Notes = ?")
        params.append(notes)

    if not fields:
        return False

    params.append(log_id)

    with get_connection() as conn:
        cursor = conn.cursor()
        query = f"UPDATE Habits_log SET {', '.join(fields)} WHERE Log_ID = ?"
        cursor.execute(query, tuple(params))
        conn.commit()
        return True


def delete_log(log_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Habits_log WHERE Log_ID = ?", (log_id,))
        conn.commit()
