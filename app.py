from database.database_manager import initialize_database
from ui.main_window import start_ui

def main():
    initialize_database()
    start_ui()

if __name__ == "__main__":
    main()