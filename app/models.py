from sqlalchemy import Column, Integer, String, Date, Time, ARRAY
from app.database import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    round = Column(String)           # "Matchday 1"
    date = Column(Date)
    time = Column(Time)
    team1 = Column(String)
    team2 = Column(String)
    score_ft = Column(ARRAY(Integer))  # [0, 2]
    score_ht = Column(ARRAY(Integer))
    group = Column(String)           # "Group A"
    ground = Column(String)          # "Al Bayt Stadium"
    tournament = Column(String)      # "World Cup 2026"