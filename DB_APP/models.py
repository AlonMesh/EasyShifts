from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)  # TODO: Use uuid
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)  # TODO: Hashing passwords
    isManager = Column(Boolean, nullable=False)
    stillWorks = Column(Boolean, nullable=False)
    # TODO: ADD WORK ID!!!
    # createdAt = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    # TODO: Validation, Error Handling
