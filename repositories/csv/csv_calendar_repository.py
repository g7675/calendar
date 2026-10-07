import csv
from datetime import datetime, time
from pathlib import Path

from models.event import Event
from models.time_range import TimeRange
from repositories.calendar_repository import CalendarRepository


class CsvCalendarRepository(CalendarRepository):

    def __init__(self, file_path: str | Path):
        self._file_path = Path(file_path)

    def get_events(self) -> list[Event]:
        events = []

        with self._file_path.open(
            newline="",
            encoding="utf-8",
        ) as file:
            reader = csv.reader(file)

            next(reader, None)

            for row in reader:
                person, subject, start, end = row

                events.append(
                    Event(
                        person=person,
                        subject=subject,
                        time_range=TimeRange(
                            start=self._parse_time(start),
                            end=self._parse_time(end),
                        ),
                    )
                )

        return events

    @staticmethod
    def _parse_time(value: str) -> time:
        return datetime.strptime(
            value.strip(),
            "%H:%M",
        ).time()