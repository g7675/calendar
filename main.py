from datetime import time, timedelta
from pathlib import Path

from repositories.csv import CsvCalendarRepository
from services.calendar_service import CalendarService


def find_available_slots(
    person_list: list[str],
    event_duration: timedelta,
) -> list[time]:
    csv_path = Path(__file__).parent / "data" / "calendar.csv"

    repository = CsvCalendarRepository(csv_path)
    service = CalendarService(repository)

    return service.find_available_slots(
        person_list=person_list,
        event_duration=event_duration,
    )


if __name__ == "__main__":
    result = find_available_slots(
        person_list=["Alice", "Jack"],
        event_duration=timedelta(hours=1),
    )

    for start_time in result:
        print(start_time.strftime("%H:%M"))