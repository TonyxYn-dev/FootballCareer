from dataclasses import dataclass
from datetime import date, timedelta

@dataclass
class WorldClock:
    """Calendar primitive. Time-step rules remain TODO(design)."""
    current_date: str

    def today(self) -> date:
        return date.fromisoformat(self.current_date)

    def advance_days(self, days: int):
        if days < 0:
            raise ValueError("World time cannot move backwards.")
        self.current_date = (self.today() + timedelta(days=days)).isoformat()
