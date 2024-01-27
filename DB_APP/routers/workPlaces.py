from fastapi import APIRouter, Depends, HTTPException, FastAPI
from pydantic import BaseModel
from sqlalchemy.orm import Session

from DB_APP.db import models
from DB_APP.db.models import WorkPlace
from DB_APP.db.session import get_db, engine

router = APIRouter()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


# class WorkPlaces(BaseModel):

@router.post("/")
def create_entity(user_id: int, work_place_id: int, db: Session = Depends(get_db)):
    new_entity = WorkPlace()
    new_entity.userID = user_id
    new_entity.workPlaceID = work_place_id

    db.add(new_entity)
    db.commit()
    db.refresh(new_entity)

    return new_entity


@router.get("/")
def get_work_places(db: Session = Depends(get_db)):
    return db.query(WorkPlace).all()


@router.get("/user_id/")
def get_work_place_of_user(user_id: int, db: Session = Depends(get_db)):
    work_place = db.query(WorkPlace).filter(WorkPlace.userID == user_id).first()
    if not work_place:
        raise HTTPException(status_code=404, detail="Work place not found")
    return work_place
