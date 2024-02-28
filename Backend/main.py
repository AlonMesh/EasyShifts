from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.db.models import Base
from Backend.config.private_password import PASSWORD  # Create this file locally, set private_password.py = ... and DON'T upload to GitHub!


def initialize_database_and_session():
    """
    Explanation:

    - **create_engine():** Establishes a connection to the MySQL database file "easyshiftsdb".
    - **sessionmaker():** Constructs a session factory that creates new sessions tied to the engine.
        - `autocommit=False`: Prevents automatic commits for each operation, allowing for control over transactions.
        - `autoflush=False`: Delays flushing changes to the database until explicitly committed, potentially improving performance.
    """
    # Create a SQLAlchemy engine and session
    engine = create_engine(
        f'mysql+pymysql://root:{PASSWORD}@localhost:3306/easyshiftsdb')  # Connect to a MySQL database
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    create_tables(engine)

    # Creating a session object
    db = SessionLocal()

    return db, SessionLocal


def create_tables(engine):
    # Create all tables if they don't exist
    Base.metadata.create_all(bind=engine)
