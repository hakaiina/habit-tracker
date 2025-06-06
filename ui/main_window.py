import customtkinter as ctk
from pyexpat.errors import messages

from databases import db_manager
from ui.habit_form import HabitForm
from ui.calendar_view import CalendarView
from ui.stats_view import StatsView
from datetime import datetime

class MainWindow(ctk.CTk):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.title("Трекер привычек")
        self.geometry("1000x500")
        self.resizable(False, False)

        self.create_widgets()
        self.load_habits()

    def create_widgets(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=680, height=400)
        self.scrollable_frame.pack(pady=20)

        self.add_button = ctk.CTkButton(self, text="Добавить привычку", command=self.open_add_habit_window)
        self.add_button.pack(pady=10)

    def load_habits(self):
        # Очистка фрейма
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        habits = db_manager.get_habits_by_user(self.user_id)
        if not habits:
            no_data_label = ctk.CTkLabel(self.scrollable_frame, text="Нет добавленных привычек.")
            no_data_label.pack(pady=20)
            return

        for habit in habits:
            frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
            frame.pack(fill='x', padx=10, pady=5)

            name_label = ctk.CTkLabel(frame, text=habit["Name_habit"], font=("Arial", 16, "bold"))
            name_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

            button_frame = ctk.CTkFrame(frame, fg_color="transparent")
            button_frame.grid(row=0, column=1, sticky="e", padx=10)

            ctk.CTkButton(button_frame, text="✅ Выполнить", width=100,
                          command=lambda h=habit: self.mark_habit_done(h)).pack(side="left", padx=2)

            ctk.CTkButton(button_frame, text="✏️ Редактировать", width=110,
                          command=lambda h=habit: self.open_edit_habit_window(h)).pack(side="left", padx=2)

            ctk.CTkButton(button_frame, text="🗑 Удалить", width=80,
                          command=lambda h=habit: self.delete_habit(h["Habit_ID"])).pack(side="left", padx=2)

            ctk.CTkButton(button_frame, text="📊 Статистика", width=100,
                          command=lambda h=habit: self.open_stats(h)).pack(side="left", padx=2)

            ctk.CTkButton(button_frame, text="📅 Календарь", width=90,
                          command=lambda h=habit: self.open_calendar(h)).pack(side="left", padx=2)

    def open_add_habit_window(self):
        HabitForm(self, self.user_id, on_save=self.load_habits)

    def open_edit_habit_window(self, habit):
        HabitForm(self, self.user_id, habit=habit, on_save=self.load_habits)

    def delete_habit(self, habit_id):
        db_manager.delete_habit(habit_id)
        self.load_habits()

    def open_calendar(self, habit):
        CalendarView(self, habit["Habit_ID"])

    def open_stats(self, habit):
        StatsView(self, habit)

    def mark_habit_done(self, habit):
        today = datetime.now().date().isoformat()

        existing_logs = db_manager.get_habit_log_by_date(habit["Habit_ID"], today)
        if existing_logs:
            ctk.CTkMessagebox(title="Уже выполнено", message="Привычка уже отмечена на сегодня")
            return

        db_manager.log_habit_status(
            habit_id = habit["Habit_ID"],
            status_id=1,
            date_start=today,
            date_end=today,
            notes=""
        )
        ctk.CTkMessagebox(title="Успех", message="Привычка отмечена как выполненная")