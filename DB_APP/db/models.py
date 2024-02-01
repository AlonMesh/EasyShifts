from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, PrimaryKeyConstraint
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    """Represents a user in the system."""
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True)
    username = Column(String(20), unique=True, nullable=False)
    password = Column(String(20), nullable=False)  # TODO: Hashing passwords
    isManager = Column(Boolean, nullable=False)
    isActive = Column(Boolean, nullable=False)
    name = Column(String(20), nullable=False)


class WorkPlace(Base):
    """Represents a workplace associated with a user."""
    __tablename__ = "workPlaces"

    userID = Column(Integer, primary_key=True, index=True, nullable=False)
    workPlaceID = Column(Integer, nullable=False)


class UserRequest(Base):
    """Represents user request for shifts."""
    __tablename__ = "userRequests"

    userID = Column(Integer, primary_key=True, index=True)
    modifyAt = Column(DateTime, nullable=False)
    requests = Column(String(30), nullable=False)


class ShiftPart(Enum):
    """Represents possible shift parts."""
    Morning = 'morning'
    Noon = 'noon'
    Evening = 'evening'


class Shift(Base):
    """Represents shifts in the system."""
    __tablename__ = "shifts"

    shiftID = Column(Integer, primary_key=True, index=True)
    workPlaceID = Column(Integer, nullable=False)
    shiftDate = Column(DateTime, nullable=False)
    shiftPart = Column(String(10), nullable=False)


class ShiftWorker(Base):
    """Represents all shifts of all workers."""
    __tablename__ = "shiftWorkers"

    shiftID = Column(Integer, nullable=False)
    userID = Column(Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('shiftID', 'userID'),
    )
