from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional, List


# --- Grupos ---
class GroupOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# --- Usuarios ---
class UserCreate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    password: str
    group_ids: Optional[List[int]] = []  # IDs de grupos a los que pertenece


class UserOut(BaseModel):
    id: int
    username: str
    first_name: str
    last_name: str
    email: str
    is_active: bool
    groups: List[GroupOut] = []

    class Config:
        from_attributes = True


# --- Goles ---
class Goal(BaseModel):
    name: str
    minute: int
    penalty: Optional[bool] = None
    offset: Optional[int] = None  # minutos extra (ej. 90+9)


# --- Match ---
class MatchOut(BaseModel):
    id: int
    num: Optional[int] = None
    round: str
    date: date
    time_local: str
    team1: str
    team2: str
    group: Optional[str] = None
    ground: str
    tournament: str

    # Resultados (null antes del partido)
    score_ft: Optional[List[int]] = None
    score_ht: Optional[List[int]] = None
    goals1: Optional[List[Goal]] = None
    goals2: Optional[List[Goal]] = None
    finished: bool = False

    class Config:
        from_attributes = True


class MatchCreate(BaseModel):
    """Para insertar un partido manualmente vía POST"""

    num: Optional[int] = None
    round: str
    date: date
    time_local: str
    team1: str
    team2: str
    group: Optional[str] = None
    ground: str
    tournament: str = "World Cup 2026"


class MatchUpdate(BaseModel):
    """Para actualizar resultado después del partido"""

    score_ft: Optional[List[int]] = None
    score_ht: Optional[List[int]] = None
    goals1: Optional[List[Goal]] = None
    goals2: Optional[List[Goal]] = None
    finished: Optional[bool] = None
