from sqlalchemy import Column, Integer, String, Date, JSON, Boolean
from app.database import Base

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
