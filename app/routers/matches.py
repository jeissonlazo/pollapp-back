from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from typing import Optional

router = APIRouter(prefix="/matches", tags=["Matches"])


# GET /matches/ → todos los partidos (con filtros opcionales)
@router.get("/", response_model=list[schemas.MatchOut])
def get_matches(
    round: Optional[str] = Query(None, example="Matchday 1"),
    group: Optional[str] = Query(None, example="Group A"),
    finished: Optional[bool] = Query(None),
    db: Session = Depends(get_db),
):
    query = db.query(models.Match)
    if round:
        query = query.filter(models.Match.round == round)
    if group:
        query = query.filter(models.Match.group == group)
    if finished is not None:
        query = query.filter(models.Match.finished == finished)
    return query.order_by(models.Match.date).all()


# GET /matches/{id} → un partido por ID
@router.get("/{match_id}", response_model=schemas.MatchOut)
def get_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    return match


# POST /matches/ → crear un partido manualmente
@router.post("/", response_model=schemas.MatchOut, status_code=201)
def create_match(match_in: schemas.MatchCreate, db: Session = Depends(get_db)):
    match = models.Match(**match_in.model_dump())
    db.add(match)
    db.commit()
    db.refresh(match)
    return match


# PATCH /matches/{id}/result → cargar resultado al terminar el partido
@router.patch("/{match_id}/result", response_model=schemas.MatchOut)
def update_result(
    match_id: int, result: schemas.MatchUpdate, db: Session = Depends(get_db)
):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado")

    update_data = result.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(match, field, value)

    db.commit()
    db.refresh(match)
    return match


# DELETE /matches/{id} → eliminar un partido
@router.delete("/{match_id}", status_code=204)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Partido no encontrado")
    db.delete(match)
    db.commit()
