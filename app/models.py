from sqlalchemy import Column, Integer, String, Date, JSON, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.database import Base

# Tabla intermedia (muchos a muchos: usuario ↔ grupo)
user_groups = Table(
    "user_groups",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("group_id", Integer, ForeignKey("groups.id"), primary_key=True),
)

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    invite_code = Column(String, unique=True, nullable=False, index=True)
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    admin = relationship("User", foreign_keys=[admin_id])
    members = relationship("User", secondary=user_groups, back_populates="groups")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)  # se guardará hasheada
    is_active = Column(Boolean, default=True)

    groups = relationship("Group", secondary=user_groups, back_populates="users")


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    num = Column(Integer, nullable=True)  # número de partido (eliminatorias)
    round = Column(String)  # "Matchday 1", "Quarter-final", etc.
    date = Column(Date)
    time_local = Column(String)  # "13:00 UTC-6" tal como viene
    team1 = Column(String)
    team2 = Column(String)
    group = Column(String, nullable=True)  # null en eliminatorias
    ground = Column(String)
    tournament = Column(String, default="World Cup 2026")

    # Se llenan después del partido
    score_ft = Column(JSON, nullable=True)  # [0, 2]
    score_ht = Column(JSON, nullable=True)  # [0, 0]
    goals1 = Column(JSON, nullable=True)  # [{"name": "...", "minute": 84}]
    goals2 = Column(JSON, nullable=True)
    finished = Column(Boolean, default=False)
