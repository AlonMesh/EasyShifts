from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from uuid import UUID
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

MIN_LEN = 1
MAX_LEN = 30

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class User(BaseModel):
    # ID is taken cared automatically
    username: str = Field(default=..., min_length=MIN_LEN, max_length=MAX_LEN)
    password: str = Field(default=..., min_length=MIN_LEN, max_length=MAX_LEN)
    isManager: bool = Field(default=False)
    stillWorks: bool = Field(default=True)
    # createdAt: datetime


@app.get("/")
def read_api(db: Session = Depends(get_db)):
    return db.query(models.Users).all()


@app.post("/")
def create_user(user: User, db: Session = Depends(get_db)):
    # Create a similar object according to the db
    user_model = models.Users()
    user_model.username = user.username
    user_model.password = user.password
    user_model.stillWorks = user.stillWorks
    user_model.isManager = user.isManager

    # Add the new object to the db
    db.add(user_model)
    db.commit()

    return user


def get_user_model_by_user(user_id: UUID, db: Session = Depends(get_db)):
    # Find the wished user
    user_model = db.query(models.Users).filter(models.Users.id == user_id).first()

    # In case this user does not exists raise an error
    if user_model is None:
        raise HTTPException(
            status_code=404,
            detail=f'ID {user_id} does not exists'
        )

    return user_model


@app.put("/{user_id}")
def update_user(user_id: UUID, user: User, db: Session = Depends(get_db)):
    # Get a pointer to the wished user (to be updated)
    user_model = get_user_model_by_user(user_id, db)

    # Set its fields according to the user object
    user_model.username = user.username
    user_model.password = user.password

    # Update the db
    db.add(user_model)
    db.commit()
    return user


@app.delete("/{user_id}")
def delete_user(user_id: UUID, db: Session = Depends(get_db)):
    # Check if the user exists by the next function
    get_user_model_by_user(user_id, db)

    # Delete the wished user by its id and update the db
    db.query(models.Users).filter(models.Users.id == user_id).delete()
    db.commit()
