from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()

NAMES_LEN = 20
PASS_LEN = 50

class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (int): Unique identifier for the user.
        username (str): User's unique username.
        password (str): User's password (TODO: Hashing passwords).
        isManager (bool): Indicates if the user is a manager.
        isActive (bool): Indicates if the user account is active.
        name (str): User's name.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, nullable=False)  # userID
    username = Column(String(NAMES_LEN), unique=True, nullable=False)
    password = Column(String(PASS_LEN), nullable=False)  # TODO: Hashing passwords
    isManager = Column(Boolean, nullable=False)
    isActive = Column(Boolean, nullable=False)
    name = Column(String(NAMES_LEN), nullable=False)


class WorkPlace(Base):
    """
    Represents a workplace associated with a user.

    Attributes:
        id (int): Unique identifier for the user.
        workPlaceID (int): Unique identifier for the workplace association.
    """
    __tablename__ = "workPlaces"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True, nullable=False)  # userID
    workPlaceID = Column(Integer, nullable=False)


class UserRequest(Base):
    """
    Represents user request for shifts.

    Attributes:
        id (int): Unique identifier for the user that send the request.
        modifyAt (DateTime): Date and time of the modification.
        requests (str): User's request details.
    """
    __tablename__ = "userRequests"

    id = Column(Integer, ForeignKey('users.id'), primary_key=True, index=True)  # userID
    modifyAt = Column(DateTime)
    requests = Column(String(255))


class ShiftPart(Enum):
    """Represents possible shift parts."""
    Morning = 'morning'
    Noon = 'noon'
    Evening = 'evening'


class Shift(Base):
    """
    Represents shifts in the system.

    Attributes:
        id (int): Unique identifier for the shift.
        workPlaceID (int): Identifier for the associated workplace.
        shiftDate (DateTime): Date and time of the shift.
        shiftPart (str): Part of the day for the shift (e.g., 'morning', 'noon', 'evening').
    """
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)  # shiftID
    workPlaceID = Column(Integer, nullable=False)
    shiftDate = Column(DateTime, nullable=False)
    shiftPart = Column(String(10), nullable=False)


class ShiftWorker(Base):
    """
    Represents all shifts of all workers.

    Attributes:
        shiftID (int): ID of the associated shift.
        userID (int): ID of the associated user.
    """
    __tablename__ = "shiftWorkers"

    shiftID = Column(Integer, ForeignKey('shifts.id'), nullable=False)
    userID = Column(Integer, ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('shiftID', 'userID'),
    )
