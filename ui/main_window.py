import customtkinter as ctk
import tkinter.messagebox as messagebox
from databases import db_manager
from ui.habit_form import HabitForm

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("dark-blue")

class MainWindow(ctk.CTk):


    def __init__(self, user_id):
        super().__init__()

        self.user_id = user_id
        self.title("Трекер привычек")
        self.geometry("800x600")
        self.resizable(False, False)

        self.create_widgets()
        self.load_habits()


    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Мои привычки", font=("Arial", 24))
        self.title_label.pack(pady=10)

        self.habit_listbox = ctk.CTkScrollableFrame(self, width=700, height=400)
        self.habit_listbox.pack(pady=10)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        self.add_button = ctk.CTkButton(button_frame, text="Добавить", command=self.add_habit)
        self.add_button.grid(row=0, column=0, padx=10)

        self.edit_button = ctk.CTkButton(button_frame, text="Редактировать", command=self.edit_habit)
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ctk.CTkButton(button_frame, text="Удалить", command=self.delete_habit)
        self.delete_button.grid(row=0, column=2, padx=10)


    def load_habits(self):
        for widget in self.habit_listbox.winfo_children():
            widget.destroy()

        habits = db_manager.get_all_habits(self.user_id)

        for habit in habits:
            habit_id, _, name, desc, _, _ = habit
            frame = ctk.CTkFrame(self.habit_listbox)
            frame.pack(fill="x", pady=5, padx=10)

            label = ctk.CTkLabel(frame, text=name, font=("Arial", 16))
            label.pack(side="left", padx=5)

            mark_button = ctk.CTkButton(frame, text="Выполнено", width=100, command=lambda h_id=habit_id: self.mark_done(h_id))
            mark_button.pack(side="right", padx=5)


    def add_habit(self):
        HabitForm(self, user_id=self.user_id, on_save=self.load_habits)


    def edit_habit(self):
        messagebox.showinfo("Редактировать", "Окно редактирования привычки")


    def delete_habit(self):
        messagebox.showinfo("Удалить", "Удаление привычки")


    def mark_done(self, habit_id):
        db_manager.add_habit_log(habit_id=habit_id, status_id=1)
        messagebox.showinfo("Готово", "Привычка выполнена")

