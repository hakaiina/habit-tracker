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

# Изменяем log_habit_status
def log_habit_status(habit_id, completed=True, log_date=None, notes=None):
    with get_connection() as conn:
        cursor = conn.cursor()
        log_date = log_date or datetime.now().strftime('%Y-%m-%d')
        status = 'completed' if completed else 'skipped'
        cursor.execute('''
            INSERT INTO habits_log (habit_id, status, log_date, notes)
            VALUES (?, ?, ?, ?)
        ''', (habit_id, status, log_date, notes))
        conn.commit()


def get_habit_stats(self, habit_id):
    """Возвращает статистику по привычке"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Текущая серия выполнений
        cursor.execute('''
            WITH RECENT_DAYS AS (
                SELECT log_date 
                FROM habits_log 
                WHERE habit_id = ? AND status = 'completed'
                ORDER BY log_date DESC
                LIMIT 30
            )
            SELECT COUNT(*) FROM RECENT_DAYS
            WHERE date(log_date) >= date('now', '-30 days')
        ''', (habit_id,))
        current_streak = cursor.fetchone()[0]

        # Общий процент успеха
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 / 
                NULLIF(COUNT(*), 0)
            FROM habits_log 
            WHERE habit_id = ?
        ''', (habit_id,))
        success_rate = round(cursor.fetchone()[0] or 0, 1)

        # Процент выполнения за последний месяц
        cursor.execute('''
            SELECT 
                COUNT(CASE WHEN status = 'completed' THEN 1 END) * 100.0 / 
                NULLIF(COUNT(*), 0)
            FROM habits_log 
            WHERE habit_id = ? AND date(log_date) >= date('now', '-30 days')
        ''', (habit_id,))
        monthly_completion = round(cursor.fetchone()[0] or 0, 1)

        return {
            'current_streak': current_streak,
            'success_rate': success_rate,
            'monthly_completion': monthly_completion
        }


def get_habit_logs(self, habit_id, days=30):
    """Возвращает логи привычки за указанный период"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT log_date, status 
            FROM habits_log 
            WHERE habit_id = ? 
            AND date(log_date) >= date('now', ? || ' days')
            ORDER BY log_date DESC
        ''', (habit_id, f'-{days}'))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]


def get_enhanced_stats(habit_id):
    """Возвращает расширенную статистику по привычке"""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Общее количество выполнений
        cursor.execute('''
            SELECT COUNT(*) FROM habits_log 
            WHERE habit_id = ? AND status = 'completed'
        ''', (habit_id,))
        total_completed = cursor.fetchone()[0]

        # Максимальная серия выполнений
        cursor.execute('''
            WITH dates AS (
                SELECT date(log_date) as day 
                FROM habits_log 
                WHERE habit_id = ? AND status = 'completed'
                GROUP BY day
                ORDER BY day
            ),
            grouped AS (
                SELECT day,
                       julianday(day) - julianday('1970-01-01') - 
                       ROW_NUMBER() OVER (ORDER BY day) as grp
                FROM dates
            )
            SELECT MAX(streak) as max_streak
            FROM (
                SELECT COUNT(*) as streak
                FROM grouped
                GROUP BY grp
            )
        ''', (habit_id,))
        max_streak = cursor.fetchone()[0] or 0

        # Выполнения за последнюю неделю
        cursor.execute('''
            SELECT COUNT(*) FROM habits_log
            WHERE habit_id = ? AND status = 'completed'
            AND date(log_date) >= date('now', '-7 days')
        ''', (habit_id,))
        current_week = cursor.fetchone()[0] or 0

        # Выполнения за последний месяц
        cursor.execute('''
            SELECT COUNT(*) FROM habits_log
            WHERE habit_id = ? AND status = 'completed'
            AND date(log_date) >= date('now', '-30 days')
        ''', (habit_id,))
        current_month = cursor.fetchone()[0] or 0

        return {
            'total_completed': total_completed,
            'max_streak': max_streak,
            'current_week': current_week,
            'current_month': current_month
        }

def get_habit_logs_by_period(habit_id, start_date, end_date):
    """Возвращает логи привычки за указанный период"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT log_date, status 
            FROM habits_log 
            WHERE habit_id = ? 
            AND log_date BETWEEN ? AND ?
            ORDER BY log_date
        ''', (habit_id, start_date, end_date))
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]