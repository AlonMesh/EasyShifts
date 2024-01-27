from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DB_APP.private_password import PASSWORD  # Create this file locally and don't upload to GitHub

"""
Explanation:

- **get_db():** This function provides a context manager for creating and closing database sessions efficiently.
    - It uses the `yield` keyword to create a session, temporarily pause execution, and return the session to the caller.
    - When the caller exits the context block (e.g., using a `with` statement), execution resumes within the `finally` block, ensuring the session is closed even if exceptions occur.
- **create_engine():** Establishes a connection to the MySQL database file "easyshiftsdb".
- **sessionmaker():** Constructs a session factory that creates new sessions tied to the engine.
    - `autocommit=False`: Prevents automatic commits for each operation, allowing for control over transactions.
    - `autoflush=False`: Delays flushing changes to the database until explicitly committed, potentially improving performance.
"""


def get_db():
    """
    Creates a database session using a context manager.

    Yields:
        Session: A SQLAlchemy session object.
    """
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Create the database engine
engine = create_engine(f'mysql+pymysql://root:{PASSWORD}@localhost:3306/easyshiftsdb')  # Connect to a MySQL database

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
