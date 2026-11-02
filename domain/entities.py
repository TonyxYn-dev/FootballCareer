from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class Player:
    player_id: str
    full_name: str
    date_of_birth: str
    nationality_code: str
    position_code: str
    club_id: Optional[str] = None
    data_origin: str = "user_created"
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    retrieved_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Club:
    club_id: str
    name: str
    country_code: str
    league_id: Optional[str] = None
    data_origin: str = "imported"
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    retrieved_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)

@dataclass
class Competition:
    competition_id: str
    name: str
    country_code: str
    competition_type: str
    data_origin: str = "imported"
    source_name: Optional[str] = None
    source_url: Optional[str] = None
    retrieved_at: Optional[str] = None

    def to_dict(self):
        return asdict(self)
