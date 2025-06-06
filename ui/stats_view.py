import customtkinter as ctk
from databases import db_manager
from datetime import datetime

class StatsView(ctk.CTkToplevel):
    def __init__(self, master, habit):
        super().__init__(master)
        self.habit = habit
        self.title(f"Статистика: {habit['Name_habit']}")
        self.geometry("400x300")
        self.resizable(False, False)

        self.create_widgets()
        self.display_stats()

    def create_widgets(self):
        self.label_title = ctk.CTkLabel(self, text="Статистика выполнения", font=("Arial", 18, "bold"))
        self.label_title.pack(pady=10)

        self.label_completed = ctk.CTkLabel(self, text="")
        self.label_completed.pack(pady=5)

        self.label_total = ctk.CTkLabel(self, text="")
        self.label_total.pack(pady=5)

        self.label_percentage = ctk.CTkLabel(self, text="")
        self.label_percentage.pack(pady=5)

        self.label_days_active = ctk.CTkLabel(self, text="")
        self.label_days_active.pack(pady=5)

    def display_stats(self):
        progress = db_manager.get_progress_by_habit(self.habit["Habit_ID"])
        total_records = len(progress)
        completed_count = sum(1 for p in progress if p[1] == 1)

        if total_records > 0:
            percent = (completed_count / total_records) * 100
        else:
            percent = 0

        # Дата начала привычки
        create_date = datetime.strptime(self.habit["Create_date"], "%Y-%m-%d")
        days_active = (datetime.now().date() - create_date.date()).days

        # Вывод
        self.label_completed.configure(text=f"Выполнено: {completed_count} раз(а)")
        self.label_total.configure(text=f"Всего записей: {total_records}")
        self.label_percentage.configure(text=f"Процент выполнения: {percent:.2f}%")
        self.label_days_active.configure(text=f"Дней с начала: {days_active}")