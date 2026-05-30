from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.get("/matchday/{round_number}", response_model=list[schemas.MatchOut])
def get_matchday(round_number: int, db: Session = Depends(get_db)):
    return db.query(models.Match)\
            .filter(models.Match.round == f"Matchday {round_number}")\
            .all()