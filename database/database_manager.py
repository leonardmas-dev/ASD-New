from sqlalchemy import create_engine, inspect, text
from database.models import Base
from utils.config import DB_URL, DB_NAME

def initialize_database():
    # Connect without selecting DB
    engine_no_db = create_engine(DB_URL.replace(f"/{DB_NAME}", ""))

    with engine_no_db.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
        conn.execute(text(f"USE {DB_NAME};"))

    # connect to actual DB
    engine = create_engine(DB_URL)
    inspector = inspect(engine)

    # get tables
    existing_tables = inspector.get_table_names()
    model_tables = list(Base.metadata.tables.keys())

    # If table count or names differ then it will be rebuilt again
    if set(existing_tables) != set(model_tables):
        print("Table mismatch detected — rebuilding database...")
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        print("Database updated.")
        return engine

    # columns check for every table
    for table_name, table in Base.metadata.tables.items():
        model_columns = set(table.columns.keys())
        db_columns = set(col["name"] for col in inspector.get_columns(table_name))

        if model_columns != db_columns:
            print(f"Column mismatch detected in '{table_name}' — rebuilding database...")
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)
            print("Database updated.")
            return engine

    print("No database changes detected.")
    return engine