import calendar
from datetime import date, datetime
import customtkinter as ctk
from databases import db_manager

class CalendarView(ctk.CTkToplevel):
    def __init__(self, master, user_id):
        super().__init__(master)
        self.title("Календарь привычек")
        self.geometry("500x500")
        self.resizable(False, False)

        self.user_id = user_id
        self.today = date.today()
        self.current_year = self.today.year
        self.current_month = self.today.month

        self.create_widgets()
        self.load_calendar()

    def create_widgets(self):
        self.title_label = ctk.CTkLabel(self, text="Календарь выполнения", font=("Arial", 20))
        self.title_label.pack(pady=20)

        self.calendar_frame = ctk.CTkFrame(self)
        self.calendar_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def load_calendar(self):
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        habit_logs = db_manager.get_habit_logs_by_user(self.user_id)

        log_map = {}
        for log in habit_logs:
            log_date = datetime.strptime(log['Date_start'], '%Y-%m-%d').date()
            status = log['Name status']
            log_map[log_date] = status

        cal = calendar.Calendar()
        days = cal.itermonthdays(self.current_year, self.current_month)

        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for idx, name in enumerate(days_of_week):
            label = ctk.CTkLabel(self.calendar_frame, text=name)
            label.grid(row=0, column=idx, padx=5, pady=2)

        row = 1
        col = 0
        for day in days:
            if day == 0:
                col += 1
                continue

            date_obj = date(self.current_year, self.current_month, day)
            status = log_map.get(date_obj, "Нет данных")

            color_map = {
                "Выполнено": "4CAF50",
                "Пропущено": "F44336",
                "Нет данных": "FFFFFF"
            }
            btn_color = color_map.get(status, "FFFFFF")

            day_btn = ctk.CTkButton(
                self.calendar_frame,
                text=str(day),
                fg_color=btn_color,
                text_color="black",
                hover=False,
                width=40,
                height=40
                )
            day_btn.grid(row=row, column=col, padx=2, pady=2)

            col += 1
            if col > 6:
                col = 0
                row += 1