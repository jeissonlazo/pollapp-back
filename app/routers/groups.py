from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas
from app.auth import get_current_user
import secrets

router = APIRouter(prefix="/groups", tags=["Groups"])


# POST /groups/ → crear grupo (requiere login)
@router.post("/", response_model=schemas.GroupOut, status_code=201)
def create_group(
    group_in: schemas.GroupCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    invite_code = secrets.token_urlsafe(8)  # ej: "aB3kR9xZ"

    group = models.Group(
        name=group_in.name,
        invite_code=invite_code,
        admin_id=current_user.id,
    )
    group.members.append(current_user)  # el creador es miembro automáticamente

    db.add(group)
    db.commit()
    db.refresh(group)
    return group


# POST /groups/join/{invite_code} → unirse con código
@router.post("/join/{invite_code}", response_model=schemas.GroupOut)
def join_group(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    group = (
        db.query(models.Group).filter(models.Group.invite_code == invite_code).first()
    )
    if not group:
        raise HTTPException(status_code=404, detail="Código de invitación inválido")

    if current_user in group.members:
        raise HTTPException(status_code=400, detail="Ya eres miembro de este grupo")

    group.members.append(current_user)
    db.commit()
    db.refresh(group)
    return group


# DELETE /groups/{id}/kick/{user_id} → expulsar usuario (solo admin)
@router.delete("/groups/{group_id}/kick/{user_id}", status_code=204)
def kick_member(
    group_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    if group.admin_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Solo el administrador puede expulsar usuarios"
        )

    if user_id == current_user.id:
        raise HTTPException(
            status_code=400, detail="El administrador no puede expulsarse a sí mismo"
        )

    user_to_kick = db.query(models.User).filter(models.User.id == user_id).first()
    if not user_to_kick or user_to_kick not in group.members:
        raise HTTPException(
            status_code=404, detail="El usuario no es miembro del grupo"
        )

    group.members.remove(user_to_kick)
    db.commit()


# GET /groups/ → listar todos los grupos
@router.get("/", response_model=list[schemas.GroupOut])
def get_groups(db: Session = Depends(get_db)):
    return db.query(models.Group).all()


# GET /groups/{id} → detalle de un grupo
@router.get("/{group_id}", response_model=schemas.GroupOut)
def get_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")
    return group


# GET /groups/me → mis grupos (requiere login)
@router.get("/me/groups", response_model=list[schemas.GroupOut])
def my_groups(
    db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)
):
    return current_user.groups


# POST /groups/{id}/regenerate-code → nuevo código (solo admin)
@router.post("/{group_id}/regenerate-code", response_model=schemas.GroupOut)
def regenerate_invite_code(
    group_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    group = db.query(models.Group).filter(models.Group.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Grupo no encontrado")

    if group.admin_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Solo el administrador puede regenerar el código"
        )

    group.invite_code = secrets.token_urlsafe(8)
    db.commit()
    db.refresh(group)
    return group
