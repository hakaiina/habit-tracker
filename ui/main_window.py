import customtkinter as ctk
from databases.database import Database
from models.habit import Habit
from .habit_form import HabitForm
from .styles import configure_app_theme


class MainWindow(ctk.CTk):  # Наследуем от главного класса CustomTkinter
    def __init__(self):
        super().__init__()
        self.title("Трекер привычек")  # Заголовок окна
        self.geometry("800x600")  # Размер окна
        self.styles = configure_app_theme()  # Загружаем стили
        self._setup_ui()  # Настраиваем интерфейс
        self._load_habits()  # Загружаем привычки из БД

    def _setup_ui(self):
        """Создает элементы интерфейса"""
        self.main_frame = ctk.CTkFrame(self)  # Основной контейнер
        self.main_frame.pack(fill='both', expand=True, padx=20, pady=20)

        # Кнопка добавления новой привычки
        self.add_button = ctk.CTkButton(
            self.main_frame,
            text="+ Добавить привычку",
            command=self._open_habit_form,  # Привязываем обработчик
            font=self.styles['button_font']
        )
        self.add_button.pack(pady=self.styles['pady'])

        # Прокручиваемый список для привычек
        self.habits_listbox = ctk.CTkScrollableFrame(self.main_frame)
        self.habits_listbox.pack(fill='both', expand=True)

    def _load_habits(self):
        """Загружает привычки из БД и отображает их"""
        habits = db_operations.get_all_habits()
        for habit_data in habits:
            habit = Habit(**habit_data)  # Создаем объект Habit
            self._add_habit_to_ui(habit)  # Добавляем в интерфейс

    def _add_habit_to_ui(self, habit):
        """Создает элемент интерфейса для одной привычки"""
        habit_frame = ctk.CTkFrame(self.habits_listbox)
        habit_frame.pack(fill='x', pady=5)

        # Название привычки
        ctk.CTkLabel(
            habit_frame,
            text=f"{habit.name} ({habit.periodicity})",
            font=self.styles['label_font']
        ).pack(side='left', padx=self.styles['padx'])

        # Кнопка отметки выполнения
        ctk.CTkButton(
            habit_frame,
            text="✓",
            width=30,
            command=lambda: self._mark_completed(habit.id)
        ).pack(side='right')

    def _open_habit_form(self):
        """Открывает форму добавления привычки"""
        HabitForm(self, self._refresh_habits)  # Передаем функцию обновления

    def _mark_completed(self, habit_id):
        """Отмечает привычку как выполненную"""
        db_operations.mark_habit_completed(habit_id)
        # Здесь можно добавить уведомление

    def _refresh_habits(self):
        """Обновляет список привычек"""
        for widget in self.habits_listbox.winfo_children():
            widget.destroy()  # Удаляем все элементы
        self._load_habits()  # Загружаем заново