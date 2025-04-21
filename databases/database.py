import sqlite3
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path


class Database:
    def __init__(self, db_path: str = "habits.db"):
        self.db_path = Path(db_path)
        self.connection = None

    def connect(self):
        """Устанавливает соединение с БД"""
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        return self.connection

    def close(self):
        """Закрывает соединение с БД"""
        if self.connection:
            self.connection.close()

    # ------------------- Users -------------------
    def create_user(self, username: str, email: str) -> int:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO Users (Username, Email, Reg_date) VALUES (?, ?, ?)",
                (username, email, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            return cursor.lastrowid

    # ------------------- Habits -------------------
    def create_habit(
            self,
            user_id: int,
            name: str,
            description: str = "",
            target_days: int = 7
    ) -> int:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO Habits 
                   (User_ID, Name_habit, Description, Target_days, Create_date)
                   VALUES (?, ?, ?, ?, ?)""",
                (user_id, name, description, target_days, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            )
            conn.commit()
            return cursor.lastrowid

    # ------------------- Habits_Jog -------------------
    def add_habit_log(
            self,
            habit_id: int,
            status_id: int,
            date_start: str,
            date_end: Optional[str] = None,
            notes: Optional[str] = None
    ) -> int:
        with self.connect() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO HabitsLog 
                   (Habit_ID, Status_ID, Date_start, Date_end, Notes)
                   VALUES (?, ?, ?, ?, ?)""",
                (habit_id, status_id, date_start, date_end, notes)
            )
            conn.commit()
            return cursor.lastrowid


if __name__ == "__main__":
    # Тестирование
    db = Database()
    try:
        user_id = db.create_user("test_user", "test@example.com")
        print(f"Создан пользователь с ID: {user_id}")

        habit_id = db.create_habit(user_id, "Чтение", "30 минут в день", 7)
        print(f"Создана привычка с ID: {habit_id}")

        log_id = db.add_habit_log(habit_id, 1, "2023-11-20")
        print(f"Добавлен лог с ID: {log_id}")
    finally:
        db.close()