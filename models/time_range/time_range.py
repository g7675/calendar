from dataclasses import dataclass
from datetime import time, timedelta


@dataclass(frozen=True)
class TimeRange:
    start: time
    end: time

    def duration(self) -> timedelta:
        return (
            timedelta(
                hours=self.end.hour,
                minutes=self.end.minute,
                seconds=self.end.second,
                microseconds=self.end.microsecond,
            )
            - timedelta(
                hours=self.start.hour,
                minutes=self.start.minute,
                seconds=self.start.second,
                microseconds=self.start.microsecond,
            )
        )

    def overlaps(self, other: "TimeRange") -> bool:
        return self.start < other.end and other.start < self.end

    def contains(self, other: "TimeRange") -> bool:
        return self.start <= other.start and other.end <= self.end