import customtkinter as ctk
from tkinter import messagebox
from databases import db_manager

class HabitForm(ctk.CTkToplevel):
    def __init__(self, master, user_id, habit=None, on_save=None):
        super().__init__(master)
        self.user_id = user_id
        self.habit = habit
        self.on_save = on_save
        self.title("Привычка")
        self.geometry("400x400")
        self.resizable(False, False)

        self.create_widgets()
        if self.habit:
            self.fill_form()

    def create_widgets(self):
        self.name_label = ctk.CTkLabel(self, text="Название привычки:")
        self.name_label.pack(pady=5)
        self.name_entry = ctk.CTkEntry(self, width=300)
        self.name_entry.pack(pady=5)

        self.desc_label = ctk.CTkLabel(self, text="Описание:")
        self.desc_label.pack(pady=5)
        self.desc_entry = ctk.CTkTextbox(self, width=300, height=100)
        self.desc_entry.pack(pady=5)

        self.freq_label = ctk.CTkLabel(self, text="Периодичность:")
        self.freq_label.pack(pady=5)
        self.freq_option = ctk.CTkOptionMenu(self, values=["Ежедневно", "Раз в неделю", "Раз в месяц"])
        self.freq_option.set("Ежедневно")
        self.freq_option.pack(pady=5)

        self.save_button = ctk.CTkButton(self, text="Сохранить", command=self.save_habit)
        self.save_button.pack(pady=20)

    def fill_form(self):
        self.name_entry.insert(0, self.habit["Name_habit"])
        self.desc_entry.insert("1.0", self.habit["Description"] or "")
        freq = self.habit.get("Target_days", 1)
        if freq == 1:
            self.freq_option.set("Ежедневно")
        elif freq == 7:
            self.freq_option.set("Раз в неделю")
        elif freq == 30:
            self.freq_option.set("Раз в месяц")
        else:
            self.freq_option.set("Ежедневно")

    def save_habit(self):
        name = self.name_entry.get()
        desc = self.desc_entry.get("1.0", "end").strip()
        freq_text = self.freq_option.get()
        freq_map = {
            "Ежедневно": 1,
            "Раз в неделю": 7,
            "Раз в месяц": 30
        }
        target_days = freq_map.get(freq_text, 1)

        if not name:
            messagebox.showerror("Ошибка", "Введите название привычки")
            return

        if self.habit:
            db_manager.update_habit(
                habit_id=self.habit["Habit_ID"],
                name=name,
                desc=desc,
                target_days=target_days
            )
        else:
            db_manager.add_habit(
                user_id=self.user_id,
                name=name,
                desc=desc,
                target_days=target_days
            )

        if self.on_save:
            self.on_save()

        self.destroy()