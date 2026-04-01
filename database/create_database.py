# Student: Yaseen Sassi     StudentID: 24023127

from sqlalchemy import create_engine, text
from .models import Base
from utils.config import DB_URL, DB_NAME

engine = create_engine(DB_URL.replace(f"/{DB_NAME}", ""), echo=True)

with engine.connect() as conn:
    conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};"))
    conn.execute(text(f"USE {DB_NAME};"))

engine = create_engine(DB_URL, echo=True)

Base.metadata.create_all(engine)

print("Database created successfully!")