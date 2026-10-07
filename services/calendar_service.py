from datetime import time, timedelta

from models.time_range import TimeRange
from repositories.calendar_repository import CalendarRepository


class CalendarService:
    WORKING_DAY_START = time(7, 0)
    WORKING_DAY_END = time(19, 0)

    def __init__(self, calendar_repository: CalendarRepository):
        self._calendar_repository = calendar_repository

    def find_available_slots(
        self,
        person_list: list[str],
        event_duration: timedelta,
    ) -> list[time]:
        if not person_list or event_duration <= timedelta(0):
            return []

        events = self._calendar_repository.get_events()

        relevant_events = [
            event
            for event in events
            if event.person in person_list
        ]

        busy_ranges = self._merge_ranges(
            [event.time_range for event in relevant_events]
        )

        return self._find_available_start_times(
            busy_ranges,
            event_duration,
        )

    def _merge_ranges(
        self,
        ranges: list[TimeRange],
    ) -> list[TimeRange]:
        sorted_ranges = sorted(
            ranges,
            key=lambda time_range: time_range.start,
        )

        if not sorted_ranges:
            return []

        merged_ranges = [sorted_ranges[0]]

        for current in sorted_ranges[1:]:
            previous = merged_ranges[-1]

            if previous.end >= current.start:
                merged_ranges[-1] = TimeRange(
                    start=previous.start,
                    end=max(previous.end, current.end),
                )
            else:
                merged_ranges.append(current)

        return merged_ranges

    def _find_available_start_times(
        self,
        busy_ranges: list[TimeRange],
        event_duration: timedelta,
    ) -> list[time]:
        available_start_times = []
        current_time = self.WORKING_DAY_START

        for busy_range in busy_ranges:
            if busy_range.end <= self.WORKING_DAY_START:
                continue

            if busy_range.start >= self.WORKING_DAY_END:
                break

            busy_start = max(
                busy_range.start,
                self.WORKING_DAY_START,
            )

            busy_end = min(
                busy_range.end,
                self.WORKING_DAY_END,
            )

            if current_time < busy_start:
                available_range = TimeRange(
                    start=current_time,
                    end=busy_start,
                )

                if available_range.duration() >= event_duration:
                    available_start_times.append(
                        available_range.start
                    )

            current_time = max(current_time, busy_end)

            if current_time >= self.WORKING_DAY_END:
                break

        if current_time < self.WORKING_DAY_END:
            available_range = TimeRange(
                start=current_time,
                end=self.WORKING_DAY_END,
            )

            if available_range.duration() >= event_duration:
                available_start_times.append(
                    available_range.start
                )

        return available_start_times