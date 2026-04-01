from ui.login_page import LoginPage
from database.database_manager import initialize_database

def main():
    # make sure DB is ready
    initialize_database()

    login = LoginPage()
    login.mainloop()

if __name__ == "__main__":
    main()