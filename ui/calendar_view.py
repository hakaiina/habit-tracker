import customtkinter as ctk
from tkcalendar import Calendar
from databases import db_manager

class CalendarView(ctk.CTkToplevel):
    def __init__(self, master, habit_id):
        super().__init__(master)
        self.habit_id = habit_id
        self.title("Календарь привычки")
        self.geometry("400x400")
        self.resizable(False, False)

        self.create_widgets()

    def create_widgets(self):
        self.calendar = Calendar(self, selectmode='day')
        self.calendar.pack(pady=20)

        self.mark_progress()

    def mark_progress(self):
        progress = db_manager.get_progress_by_habit(self.habit_id)
        for date_str, completed in progress:
            if completed:
                self.calendar.calevent_create(date_str, 'Выполнено', 'completed')