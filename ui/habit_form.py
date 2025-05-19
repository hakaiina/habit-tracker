import customtkinter as ctk
from tkinter import messagebox
from databases.database import Database
from .styles import configure_app_theme


class HabitForm(ctk.CTkToplevel):  # Всплывающее окно
    def __init__(self, parent, on_success):
        super().__init__(parent)
        self.title("Новая привычка")
        self.geometry("400x300")
        self.on_success = on_success  # Функция для вызова после успешного сохранения
        self.styles = configure_app_theme()
        self._setup_ui()

    def _setup_ui(self):
        """Настраивает элементы формы"""
        # Поле для названия
        ctk.CTkLabel(self, text="Название:").pack(pady=5)
        self.name_entry = ctk.CTkEntry(self)
        self.name_entry.pack(fill='x', padx=20, pady=5)

        # Радиокнопки для выбора периодичности
        ctk.CTkLabel(self, text="Периодичность:").pack(pady=5)
        self.periodicity = ctk.StringVar(value="daily")  # Значение по умолчанию
        ctk.CTkRadioButton(self, text="Ежедневно", variable=self.periodicity, value="daily").pack(anchor='w', padx=20)
        ctk.CTkRadioButton(self, text="Еженедельно", variable=self.periodicity, value="weekly").pack(anchor='w',
                                                                                                     padx=20)

        # Кнопка сохранения
        ctk.CTkButton(
            self,
            text="Сохранить",
            command=self._save_habit
        ).pack(pady=20)

    def _save_habit(self):
        """Сохраняет новую привычку в БД"""
        name = self.name_entry.get().strip()
        if not name:
            messagebox.showerror("Ошибка", "Введите название привычки")
            return

        db_operations.add_habit(name, self.periodicity.get())
        self.on_success()  # Обновляем список привычек
        self.destroy()  # Закрываем форму