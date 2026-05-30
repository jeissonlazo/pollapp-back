from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from app.database import get_db
from app import models, schemas

router = APIRouter(prefix="/users", tags=["Users"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


# POST /users/ → crear usuario
@router.post("/", response_model=schemas.UserOut, status_code=201)
def create_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):

    # Verificar duplicados
    if db.query(models.User).filter(models.User.username == user_in.username).first():
        raise HTTPException(status_code=400, detail="El username ya existe")
    if db.query(models.User).filter(models.User.email == user_in.email).first():
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    # Buscar grupos si se enviaron
    groups = []
    if user_in.group_ids:
        groups = db.query(models.Group).filter(
            models.Group.id.in_(user_in.group_ids)
        ).all()
        if len(groups) != len(user_in.group_ids):
            raise HTTPException(status_code=404, detail="Uno o más grupos no existen")

    user = models.User(
        username   = user_in.username,
        first_name = user_in.first_name,
        last_name  = user_in.last_name,
        email      = user_in.email,
        password   = hash_password(user_in.password),
        groups     = groups,
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# GET /users/ → listar usuarios
@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()


# GET /users/{id} → un usuario
@router.get("/{user_id}", response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


# PATCH /users/{id}/groups → agregar/quitar grupos
@router.patch("/{user_id}/groups", response_model=schemas.UserOut)
def update_user_groups(
    user_id: int,
    group_ids: list[int],
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    groups = db.query(models.Group).filter(models.Group.id.in_(group_ids)).all()
    user.groups = groups
    db.commit()
    db.refresh(user)
    return user