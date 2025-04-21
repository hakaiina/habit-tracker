from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class User:
    user_id: int
    username: str
    email: str
    reg_date: str

    @property
    def reg_date_formatted(self) -> str:
        return datetime.strptime(self.reg_date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')


@dataclass
class Habit:
    habit_id: int
    user_id: int
    name: str
    description: str
    target_days: int
    create_date: str

    @property
    def create_date_formatted(self) -> str:
        return datetime.strptime(self.create_date, '%Y-%m-%d %H:%M:%S').strftime('%d.%m.%Y')


@dataclass
class Status:
    status_id: int
    name: str
    description: str


@dataclass
class HabitLog:
    log_id: int
    habit_id: int
    status_id: int
    date_start: str
    date_end: Optional[str]
    notes: Optional[str]

    @property
    def date_start_formatted(self) -> str:
        return datetime.strptime(self.date_start, '%Y-%m-%d').strftime('%d.%m.%Y')

    @property
    def date_end_formatted(self) -> Optional[str]:
        if self.date_end:
            return datetime.strptime(self.date_end, '%Y-%m-%d').strftime('%d.%m.%Y')
        return None


@dataclass
class Reminder:
    reminder_id: int
    habit_id: int
    time: str
    days: str


class ModelFactory:
    @staticmethod
    def create_user_from_db(row: dict) -> User:
        return User(
            user_id=row['User_ID'],
            username=row['Username'],
            email=row['Email'],
            reg_date=row['Reg_date']
        )

    @staticmethod
    def create_habit_from_db(row: dict) -> Habit:
        return Habit(
            habit_id=row['Habit_ID'],
            user_id=row['User_ID'],
            name=row['Name_habit'],
            description=row['Description'],
            target_days=row['Target_days'],
            create_date=row['Create_date']
        )

    @staticmethod
    def create_status_from_db(row: dict) -> Status:
        return Status(
            status_id=row['Status_ID'],
            name=row['Name_status'],
            description=row.get('Description')
        )

    @staticmethod
    def create_habit_log_from_db(row: dict) -> HabitLog:
        return HabitLog(
            log_id=row['Log_ID'],
            habit_id=row['Habit_ID'],
            status_id=row['Status_ID'],
            date_start=row['Date_start'],
            date_end=row.get('Date_end'),
            notes=row.get('Notes')
        )

    @staticmethod
    def create_reminder_from_db(row: dict) -> Reminder:
        return Reminder(
            reminder_id=row['Reminder_ID'],
            habit_id=row['Habit_ID'],
            time=row['Time'],
            days=row['Days']
        )