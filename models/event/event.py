from dataclasses import dataclass

from models.time_range import TimeRange


@dataclass(frozen=True)
class Event:
    person: str
    subject: str
    time_range: TimeRange