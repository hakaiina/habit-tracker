from databases.db_manager import init_db, add_user
from ui.main_window import MainWindow
import customtkinter as ctk


if __name__ == "__main__":
    init_db()
    user_id = add_user("Тестовый пользователь")
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("themes/theme_for_app.json")
    app = MainWindow(user_id)
    app.mainloop()