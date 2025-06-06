from databases import db_manager
from ui.main_window import MainWindow
import customtkinter as ctk


if __name__ == "__main__":
    db_manager.init_db()
    user_id = 1
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("themes/theme_for_app.json")
    app = MainWindow(user_id)
    app.mainloop()