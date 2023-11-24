from datetime import datetime, timedelta
from copy import deepcopy

from src.utils.consts import WEEK_DAYS
from src.utils.helper import get_day_of_week


class ImpossibleGuard(Exception):
    def __init__(self, message="Impossible to fill planning"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def get_all_week_guard_spot(start=0, duration=24):
    guard_times = dict()
    for day in WEEK_DAYS:
        guard_times[day] = {
            'start': start,
            'duration': duration
        }

    return guard_times


class Spot:
    def __init__(self, name, guard_duration, guards_number, guard_times):
        if guard_duration > 24:
            raise ImpossibleGuard(f"The guard duration for {name} can't exceed 24 hours in a day!")

        for week_day in guard_times:
            if guard_times[week_day]['start'] > 24:
                raise ImpossibleGuard(f"The guard start for {name} for {week_day} must be inside 0 and 24 included!")

            if guard_times[week_day]['duration'] > 24:
                raise ImpossibleGuard(f"The guard time for {name} for {week_day} can't exceed 24 hours!")

        self.name = name
        self.guard_duration = guard_duration
        self.guards_number = guards_number
        self.guard_times = guard_times

    def __repr__(self):
        return f"Spot(name={self.name!r})"

    def __str__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Spot):
            return self.name == other.name

        elif isinstance(other, str):
            return self.name == other

        return False

    def __deepcopy__(self, memo=None):
        # Create a new instance with 'None' for deep attributes initially to avoid recursive deepcopy calls
        new_spot = Spot(name=self.name,
                        guard_duration=self.guard_duration,
                        guards_number=self.guards_number,
                        guard_times=self.guard_times)

        # Add the new instance to the memo dictionary to avoid recursive loops
        memo = memo or {}
        memo[id(self)] = new_spot

        # Now manually deepcopy the deep attributes without passing the memo dictionary
        new_spot.guard_times = deepcopy(self.guard_times, memo)

        return new_spot

    def __hash__(self):
        return hash(self.name)

    def is_needed(self, date):
        week_day = get_day_of_week(date)

        if week_day not in self.guard_times:
            return False

        start = date.replace(hour=self.guard_times[week_day]['start'])
        end = start + timedelta(hours=self.guard_times[week_day]['duration'])

        if start <= date < end:
            return True

        if start > date:
            prec_day = get_day_of_week(date - timedelta(days=1))

            if prec_day not in self.guard_times:
                return False

            prec_day_start = (date - timedelta(days=1)).replace(hour=self.guard_times[prec_day]['start'])
            prec_day_end = prec_day_start + timedelta(hours=self.guard_times[prec_day]['duration'])

            if prec_day_start <= date < prec_day_end:
                return True

        return False

    def find_guard_slot(self, date: datetime):
        week_day = get_day_of_week(date)

        if not self.is_needed(date):
            return None

        t = self.guard_times[week_day]['start']
        guards_total_duration = self.guard_times[week_day]['duration']

        total_duration = 0
        slot_start_date = deepcopy(date)
        slot_end_date = deepcopy(date)
        hour = date.hour

        while total_duration < guards_total_duration:
            guard_duration = 0
            while total_duration < guards_total_duration and \
                    guard_duration < self.guard_duration:
                guard_duration += 1
                guards_total_duration += 1

            slot_start_hour, slot_end_hour = t, (t + guard_duration) % 24
            t = slot_end_hour

            if slot_end_hour < slot_start_hour:
                slot_end_hour += 24

            if slot_start_hour <= hour + 24 < slot_end_hour:
                hour += 24

            if slot_start_hour <= hour < slot_end_hour:
                if slot_end_hour % 24 < slot_start_hour:
                    if hour % 24 < slot_start_hour:
                        slot_start_date -= timedelta(days=1)
                    else:
                        slot_end_date = slot_start_date + timedelta(days=1)

                return {
                    'start': slot_start_date.replace(hour=slot_start_hour),
                    'end': slot_end_date.replace(hour=slot_end_hour % 24),
                }

        return None
