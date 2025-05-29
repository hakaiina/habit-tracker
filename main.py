from databases.db_manager import init_db, add_user
from ui.main_window import MainWindow


if __name__ == "__main__":
    init_db()

    user_id = add_user("Тестовый пользователь")

    app = MainWindow(user_id)
    app.mainloop()