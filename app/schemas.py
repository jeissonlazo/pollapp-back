from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List

class MatchOut(BaseModel):
    id: int
    round: str
    date: date
    time: time
    team1: str
    team2: str
    score_ft: Optional[List[int]]
    score_ht: Optional[List[int]]
    group: str
    ground: str
    tournament: str

    class Config:
        from_attributes = True