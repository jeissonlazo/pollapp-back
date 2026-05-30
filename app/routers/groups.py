from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/groups", tags=["Groups"])


# POST /groups/ → crear grupo
@router.post("/", response_model=schemas.GroupOut, status_code=201)
def create_group(name: str, db: Session = Depends(get_db)):
    if db.query(models.Group).filter(models.Group.name == name).first():
        raise HTTPException(status_code=400, detail="El grupo ya existe")
    group = models.Group(name=name)
    db.add(group)
    db.commit()
    db.refresh(group)
    return group


# GET /groups/ → listar grupos
@router.get("/", response_model=list[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()