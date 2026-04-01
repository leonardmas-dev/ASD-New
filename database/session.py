# Student: Yaseen Sassi     StudentID: 24023127

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from utils.config import DB_URL

# Create the engine once
engine = create_engine(DB_URL, echo=False)

# Create a session
SessionLocal = sessionmaker(bind=engine)

# Function to get a new session
def get_session():
    return SessionLocal()