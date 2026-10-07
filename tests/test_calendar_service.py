from datetime import time, timedelta

from models.event import Event
from models.time_range import TimeRange
from services.calendar_service import CalendarService


class FakeCalendarRepository:
    def __init__(self, events: list[Event]):
        self._events = events

    def get_events(self) -> list[Event]:
        return self._events


def create_service(events: list[Event]) -> CalendarService:
    repository = FakeCalendarRepository(events)
    return CalendarService(repository)


def test_find_available_slots_for_multiple_people():
    events = [
        Event(
            person="Alice",
            subject="Morning meeting",
            time_range=TimeRange(time(8, 0), time(9, 30)),
        ),
        Event(
            person="Alice",
            subject="Lunch",
            time_range=TimeRange(time(13, 0), time(14, 0)),
        ),
        Event(
            person="Alice",
            subject="Yoga",
            time_range=TimeRange(time(16, 0), time(17, 0)),
        ),
        Event(
            person="Jack",
            subject="Morning meeting",
            time_range=TimeRange(time(8, 0), time(8, 50)),
        ),
        Event(
            person="Jack",
            subject="Sales call",
            time_range=TimeRange(time(9, 0), time(9, 40)),
        ),
        Event(
            person="Jack",
            subject="Lunch",
            time_range=TimeRange(time(13, 0), time(14, 0)),
        ),
        Event(
            person="Jack",
            subject="Yoga",
            time_range=TimeRange(time(16, 0), time(17, 0)),
        ),
    ]

    service = create_service(events)

    result = service.find_available_slots(
        person_list=["Alice", "Jack"],
        event_duration=timedelta(hours=1),
    )

    assert result == [
        time(7, 0),
        time(9, 40),
        time(14, 0),
        time(17, 0),
    ]


def test_returns_empty_when_person_list_is_empty():
    service = create_service([])

    result = service.find_available_slots(
        person_list=[],
        event_duration=timedelta(hours=1),
    )

    assert result == []


def test_returns_empty_when_duration_is_zero():
    service = create_service([])

    result = service.find_available_slots(
        person_list=["Alice"],
        event_duration=timedelta(0),
    )

    assert result == []


def test_returns_empty_when_duration_is_negative():
    service = create_service([])

    result = service.find_available_slots(
        person_list=["Alice"],
        event_duration=timedelta(minutes=-30),
    )

    assert result == []


def test_allows_event_ending_exactly_at_working_day_end():
    events = [
        Event(
            person="Alice",
            subject="Meeting",
            time_range=TimeRange(time(7, 0), time(18, 0)),
        ),
    ]

    service = create_service(events)

    result = service.find_available_slots(
        person_list=["Alice"],
        event_duration=timedelta(hours=1),
    )

    assert result == [time(18, 0)]


def test_adjacent_events_are_merged():
    events = [
        Event(
            person="Alice",
            subject="Meeting 1",
            time_range=TimeRange(time(8, 0), time(9, 0)),
        ),
        Event(
            person="Alice",
            subject="Meeting 2",
            time_range=TimeRange(time(9, 0), time(10, 0)),
        ),
    ]

    service = create_service(events)

    result = service.find_available_slots(
        person_list=["Alice"],
        event_duration=timedelta(hours=1),
    )

    assert result == [
        time(7, 0),
        time(10, 0),
    ]


def test_overlapping_events_are_merged():
    events = [
        Event(
            person="Alice",
            subject="Meeting 1",
            time_range=TimeRange(time(8, 0), time(9, 30)),
        ),
        Event(
            person="Alice",
            subject="Meeting 2",
            time_range=TimeRange(time(9, 0), time(10, 0)),
        ),
    ]

    service = create_service(events)

    result = service.find_available_slots(
        person_list=["Alice"],
        event_duration=timedelta(hours=1),
    )

    assert result == [
        time(7, 0),
        time(10, 0),
    ]


def test_person_with_no_events_is_available_from_start_of_working_day():
    service = create_service([])

    result = service.find_available_slots(
        person_list=["Bob"],
        event_duration=timedelta(hours=1),
    )

    assert result == [time(7, 0)]