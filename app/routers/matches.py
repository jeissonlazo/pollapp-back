from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import Optional

router = APIRouter(prefix="/matches", tags=["Matches"])


@router.get("/", response_model=list[schemas.MatchOut])
def get_matches(
    round: Optional[str] = Query(None, example="Matchday 1"),
    group: Optional[str] = Query(None, example="Group A"),
    db: Session = Depends(get_db),
):
    query = db.query(models.Match)
    if round:
        query = query.filter(models.Match.round == round)
    if group:
        query = query.filter(models.Match.group == group)
    return query.order_by(models.Match.date).all()
