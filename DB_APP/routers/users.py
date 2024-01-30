from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import DB_APP.db.models as models
from DB_APP.db.session import get_db, engine

MIN_LEN = 1
MAX_LEN = 32

router = APIRouter()

app = FastAPI()

# Create database tables
models.Base.metadata.create_all(bind=engine)


class UserBaseSchema(BaseModel):
    """User model for API requests and responses."""

    # userID is taken cared automatically
    username: str = Field(default=..., min_length=MIN_LEN, max_length=MAX_LEN)
    password: str = Field(default=..., min_length=MIN_LEN, max_length=MAX_LEN)
    isManager: bool = Field(default=False)
    isActive: bool = Field(default=True)
    name: str = Field(default="name", min_length=MIN_LEN, max_length=MAX_LEN)
    # workPlaceID: int = Field(default=...)
    # createdAt: datetime

    def verify_password(self):
        pass


@router.post("/")
def create_user(user: UserBaseSchema, db: Session = Depends(get_db)):
    """Creates a new user in the database."""

    # TODO: Implement password hashing (e.g., using Werkzeug's generate_password_hash)

    # Create database user object
    new_user = models.User()
    new_user.username = user.username
    new_user.password = user.password  # Replace with hashed password
    new_user.isActive = user.isActive
    new_user.isManager = user.isManager
    new_user.name = user.name

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Refresh to retrieve generated user ID

    return new_user


@router.get("/")
def get_users(db: Session = Depends(get_db)):
    """Retrieves all users from the database."""

    return db.query(models.User).all()


@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Retrieves a specific user by ID."""

    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
def update_user(user_id: int, user: UserBaseSchema, db: Session = Depends(get_db)):
    """Updates an existing user."""

    db_user = get_user(user_id, db)
    db_user.username = user.username
    db_user.password = user.password

    db.add(db_user)
    db.commit()
    return db_user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Deletes a user by ID."""

    get_user(user_id, db)  # Raise 404 if user not found

    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return {"detail": "User deleted successfully"}
