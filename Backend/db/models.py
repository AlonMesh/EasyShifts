import datetime
from sqlalchemy import Column, String, Boolean, Date, Enum, PrimaryKeyConstraint, ForeignKey, DateTime, JSON, func
from sqlalchemy.ext.declarative import declarative_base
from uuid import uuid4
import enum

Base = declarative_base()

NAMES_LEN = 20
PASS_LEN = 50
ID_LEN = 36
REQUEST_LEN = 255


class User(Base):
    """
    Represents a user in the system.

    Attributes:
        id (str): Unique identifier for the user.
        username (str): User's unique username.
        password (str): User's password.
        isManager (bool): Indicates if the user is a manager.
        isActive (bool): Indicates if the user account is active. Default is True.
        isApproval (bool): Indicates if the user is approved. Default is False.
        name (str): User's name.
    """
    __tablename__ = "users"

    id = Column(String(ID_LEN), primary_key=True, index=True, nullable=False, default=uuid4)  # userID
    username = Column(String(NAMES_LEN), unique=True, nullable=False)
    password = Column(String(PASS_LEN), nullable=False)
    isManager = Column(Boolean, nullable=False)
    isActive = Column(Boolean, nullable=False, default=True)
    isApproval = Column(Boolean, nullable=False, default=False)
    name = Column(String(NAMES_LEN), nullable=False)


class WorkPlace(Base):
    """
    Represents a workplace associated with a user.

    Attributes:
        id (str): Unique identifier for the user.
        workPlaceID (int): Unique identifier for the workplace association.
    """
    __tablename__ = "workPlaces"

    id = Column(String(ID_LEN), ForeignKey('users.id'), primary_key=True, index=True, nullable=False)  # userID
    workPlaceID = Column(String(ID_LEN), nullable=False)


class UserRequest(Base):
    """
    Represents user request for shifts.

    Attributes:
        id (str): Unique identifier for the user that send the request.
        modifyAt (DateTime): Date and time of the modification.
        requests (str): User's request details.
    """
    __tablename__ = "userRequests"

    id = Column(String(ID_LEN), ForeignKey('users.id'), primary_key=True, index=True)  # userID
    modifyAt = Column(DateTime)
    requests = Column(String(REQUEST_LEN))


class ShiftPart(enum.Enum):
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
        shiftDate (Date): Date and time of the shift.
        shiftPart (str): Part of the day for the shift (e.g., 'morning', 'noon', 'evening').
    """
    __tablename__ = "shifts"

    id = Column(String(ID_LEN), primary_key=True, index=True, default=uuid4)  # shiftID
    workPlaceID = Column(String(ID_LEN), nullable=False)
    shiftDate = Column(Date, nullable=False)
    shiftPart = Column(Enum(ShiftPart), nullable=False)


class ShiftWorker(Base):
    """
    Represents all shifts of all workers.

    Attributes:
        shiftID (int): ID of the associated shift.
        userID (int): ID of the associated user.
    """
    __tablename__ = "shiftWorkers"

    shiftID = Column(String(ID_LEN), ForeignKey('shifts.id'), nullable=False)
    userID = Column(String(ID_LEN), ForeignKey('users.id'), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint('shiftID', 'userID'),
    )


class ShiftBoard(Base):
    """
    Represents the workplace's shift-board.

    Attributes:
        weekStartDate (Date): Start date of the week.
        workplaceID (str): ID of the associated workplace.
        isPublished (bool): Indicates if the shift is published and visible to workers.
        content (JSON): Stores the shift-board content.
        preferences (JSON): Stores workplace's preferences/settings.
            - number_of_shifts_per_day
            - max_workers_per_shift
            - closed_days
            - etc.
        requests_window_start (DateTime): Start date and time of the requests window.
        requests_window_end (DateTime): End date and time of the requests window.
    """
    __tablename__ = "shiftBoards"

    weekStartDate = Column(Date, nullable=False, default=lambda: next_sunday())
    workplaceID = Column(String(ID_LEN), ForeignKey('users.id'), nullable=False)
    isPublished = Column(Boolean, nullable=False, default=False)
    content = Column(JSON, default=dict)
    preferences = Column(JSON, default=dict)
    requests_window_start = Column(DateTime)
    requests_window_end = Column(DateTime)

    __table_args__ = (
        PrimaryKeyConstraint('weekStartDate', 'workplaceID'),
    )


# Define the next_sunday function to be used as the default value
def next_sunday():
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday() + 7) % 7
    return today + datetime.timedelta(days=days_until_sunday)
