import customtkinter as ctk
import tkinter.messagebox as messagebox

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
        self.geometry("800x500")
        self.resizable(False, False)

        self.create_widgets()
        self.load_habits()

    def create_widgets(self):
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=700, height=400)
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
            stats = db_manager.get_enhanced_stats(habit["Habit_ID"])
            self.create_habit_widget(habit, stats)

    def create_habit_widget(self, habit, stats):
        frame = ctk.CTkFrame(self.scrollable_frame, corner_radius=10)
        frame.pack(fill='x', padx=10, pady=5, expand=True)

        # Верхняя строка - название и статистика
        top_frame = ctk.CTkFrame(frame, fg_color="transparent")
        top_frame.pack(fill='x', pady=(0, 5))

        name_label = ctk.CTkLabel(
            top_frame,
            text=f"{habit['Name_habit']} (серия: {stats['current_week']}/{habit['Target_days']})",
            font=("Arial", 14),
            anchor="w"
        )
        name_label.pack(side='left', fill='x', expand=True)

        # Нижняя строка - все кнопки
        bottom_frame = ctk.CTkFrame(frame, fg_color="transparent")
        bottom_frame.pack(fill='x')

        # Кнопки в один ряд
        buttons = [
            ("✅ Выполнить", 100, lambda h=habit: self.mark_habit_done(h)),
            ("✏️ Редактировать", 110, lambda h=habit: self.open_edit_habit_window(h)),
            ("🗑 Удалить", 80, lambda h=habit: self.delete_habit(h["Habit_ID"])),
            ("📊 Статистика", 100, lambda h=habit: self.open_stats(h)),
            ("📅 Календарь", 90, lambda h=habit: self.open_calendar(h))
        ]

        for text, width, command in buttons:
            ctk.CTkButton(
                bottom_frame,
                text=text,
                width=width,
                command=command
            ).pack(side='left', padx=2)


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

        # Проверяем, не отмечена ли уже привычка сегодня
        existing_logs = db_manager.get_habit_log_by_date(habit["Habit_ID"], today)
        if existing_logs:
            messagebox.showinfo("Информация", "Эта привычка уже отмечена сегодня")
            return

        try:
            # Логируем выполнение
            db_manager.log_habit_status(
                habit_id=habit["Habit_ID"],
                completed=True,
                log_date=today
            )

            # Обновляем интерфейс
            self.load_habits()
            messagebox.showinfo("Успех", f"Привычка '{habit['Name_habit']}' отмечена!")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось отметить привычку: {str(e)}")