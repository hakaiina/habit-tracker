import customtkinter as ctk
from databases import db_manager
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class StatsView(ctk.CTkToplevel):
    def __init__(self, master, habit):
        super().__init__(master)
        self.habit = habit
        self.title(f"Статистика: {habit['Name_habit']}")
        self.geometry("800x600")

        self.create_widgets()
        self.display_stats()

    def create_widgets(self):
        # Создаем вкладки
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill='both', expand=True, padx=10, pady=10)

        # Вкладка с общей статистикой
        self.tab_stats = self.tabview.add("Общая статистика")
        self.tab_chart = self.tabview.add("График выполнения")

        # Общая статистика
        self.stats_frame = ctk.CTkScrollableFrame(self.tab_stats)
        self.stats_frame.pack(fill='both', expand=True)

        # График
        self.chart_frame = ctk.CTkFrame(self.tab_chart)
        self.chart_frame.pack(fill='both', expand=True)

    def display_stats(self):
        # Получаем данные за последние 30 дней
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=30)
        logs = db_manager.get_habit_logs_by_period(
            self.habit["Habit_ID"],
            start_date.strftime('%Y-%m-%d'),
            end_date.strftime('%Y-%m-%d')
        )

        # Отображаем общую статистику
        self.show_general_stats(logs)

        # Отображаем график
        self.show_completion_chart(logs, start_date, end_date)

    def show_general_stats(self, logs):
        # Очищаем фрейм
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # Рассчитываем статистику
        total_days = len(logs)
        completed = sum(1 for log in logs if log['status'] == 'completed')
        completion_rate = (completed / total_days * 100) if total_days > 0 else 0

        # Отображаем статистику
        metrics = [
            ("Всего дней", total_days),
            ("Выполнено", completed),
            ("Процент выполнения", f"{completion_rate:.1f}%"),
            ("Текущая серия", self.calculate_current_streak(logs)),
            ("Максимальная серия", self.calculate_max_streak(logs))
        ]

        for label, value in metrics:
            frame = ctk.CTkFrame(self.stats_frame, fg_color="transparent")
            frame.pack(fill='x', pady=5)

            ctk.CTkLabel(frame, text=label, font=("Arial", 14)).pack(side='left')
            ctk.CTkLabel(frame, text=str(value), font=("Arial", 14, "bold")).pack(side='right')

    def show_completion_chart(self, logs, start_date, end_date):
        # Создаем данные для графика
        dates = []
        completions = []
        current_date = start_date

        while current_date <= end_date:
            date_str = current_date.strftime('%Y-%m-%d')
            completed = any(log['log_date'] == date_str and log['status'] == 'completed' for log in logs)

            dates.append(current_date)
            completions.append(1 if completed else 0)

            current_date += timedelta(days=1)

        # Создаем график
        fig, ax = plt.subplots(figsize=(8, 4))

        # Закрашиваем выполненные дни
        for i, (date, completed) in enumerate(zip(dates, completions)):
            if completed:
                ax.axvspan(date - timedelta(days=0.5),
                           date + timedelta(days=0.5),
                           color='green', alpha=0.3)

        ax.plot(dates, completions, 'o-', color='green', markersize=8, linewidth=2)
        ax.set_title(f"Выполнение '{self.habit['Name_habit']}' за последние 30 дней")
        ax.set_yticks([0, 1])
        ax.set_yticklabels(["Не выполнено", "Выполнено"])
        ax.grid(True, linestyle='--', alpha=0.7)
        ax.set_xlim(start_date - timedelta(days=1), end_date + timedelta(days=1))

        # Поворачиваем даты для лучшей читаемости
        plt.xticks(rotation=45)
        plt.tight_layout()
        # Встраиваем график в интерфейс
        canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)

    def calculate_current_streak(self, logs):
        """Рассчитывает текущую серию выполнений"""
        current_streak = 0
        today = datetime.now().date()

        for log in reversed(logs):
            log_date = datetime.strptime(log['log_date'], '%Y-%m-%d').date()
            if log['status'] == 'completed' and log_date == today - timedelta(days=current_streak):
                current_streak += 1
            else:
                break

        return current_streak

    def calculate_max_streak(self, logs):
        """Рассчитывает максимальную серию выполнений"""
        max_streak = 0
        current = 0

        for log in logs:
            if log['status'] == 'completed':
                current += 1
                max_streak = max(max_streak, current)
            else:
                current = 0

        return max_streak