from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

NAMES_LEN = 20
PASS_LEN = 50


class User(Base):
    """Represents a user in the system."""
    __tablename__ = "users"

    userID = Column(Integer, primary_key=True, index=True, nullable=False)
    username = Column(String(NAMES_LEN), unique=True, nullable=False)
    password = Column(String(PASS_LEN), nullable=False)  # TODO: Hashing passwords
    isManager = Column(Boolean, nullable=False)
    isActive = Column(Boolean, nullable=False)
    name = Column(String(NAMES_LEN), nullable=False)


class WorkPlace(Base):
    """Represents a workplace associated with a user."""
    __tablename__ = "workPlaces"

    userID = Column(Integer, ForeignKey('users.userID'), primary_key=True, index=True, nullable=False)
    workPlaceID = Column(Integer, nullable=False)


class UserRequest(Base):
    """Represents user request for shifts."""
    __tablename__ = "userRequests"

    userID = Column(Integer, ForeignKey('users.userID'), primary_key=True, index=True)
    modifyAt = Column(DateTime)
    requests = Column(String(255))


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

    shiftID = Column(Integer, ForeignKey('shifts.shiftID'), nullable=False)
    userID = Column(Integer, ForeignKey('users.userID'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('shiftID', 'userID'),
    )
