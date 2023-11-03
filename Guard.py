from itertools import cycle

# Define the week days
from consts import CRITICAL_DELAY, GUARD_SPOTS
from helper import get_prec_day, find_guard_slot

week_days = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'שבת']


class Guard:
    def __init__(self, name, partner=None, guards_slots=None,
                 not_available_times=None,
                 is_guarding=True, is_living_far_away=False,
                 spots_preferences=None, time_preferences=None,
                 last_spot=None):
        self.name = name
        self.partner = partner
        self.__guards_slots = guards_slots if guards_slots else list()
        self.__not_available_times = not_available_times \
            if not_available_times else list()

        self.is_guarding = is_guarding
        self.is_living_far_away = is_living_far_away
        self.spots_preferences = spots_preferences
        self.time_preferences = time_preferences
        self.last_spot = last_spot

    def __repr__(self):
        return f"Guard(name={self.name!r})"

    def __str__(self):
        return self.name

    def __eq__(self, other):
        if isinstance(other, Guard):
            return self.name == other.name
        return False

    def add_guard_slot(self, start, end):
        guard_obj = {
            'start': start,
            'end': end
        }

        if guard_obj not in self.__guards_slots:
            self.__guards_slots.append(guard_obj)

    def add_not_available_time(self, start, end):
        time_obj = {
            'start': start,
            'end': end
        }

        if time_obj not in self.__not_available_times:
            self.__not_available_times.append(time_obj)

    def is_missing(self, day, hour):
        for not_available_time in self.__not_available_times:
            start_day, start_hour = not_available_time['start'].values()
            end_day, end_hour = not_available_time['end'].values()

            not_available_days = get_days_list(start_day, end_day)
            not_available_hours = get_hours_list(day, start_day, end_day,
                                                 start_hour, end_hour)

            if day in not_available_days and hour in not_available_hours:
                return True

        return False

    # Helper function to check if a guard is available
    def is_available(self, watch_list, day, hour, days, spot=None, delays_prop=None):
        if not self.is_guarding:
            return False

        elif spot and self.spots_preferences \
                and spot not in self.spots_preferences:
            return False

        elif self.is_missing(day, hour):
            return False

        elif spot and self.last_spot == spot:
            return False

        elif self.time_preferences:
            in_time_preferences = False
            for time_pref in self.time_preferences:
                if time_pref['start'] <= hour < time_pref['end']:
                    in_time_preferences = True

            if not in_time_preferences:
                return False

        for rest_delay in (delays_prop if delays_prop else list(range(0, CRITICAL_DELAY + 1, 3))):
            updated_hour = hour - rest_delay
            updated_day = day

            if updated_hour < 0:
                updated_day = get_prec_day(day, days)
                updated_hour += 24

            if not updated_day:
                break

            # Check if the guard already in another spot
            for spot_name, guard_spot in GUARD_SPOTS.items():
                slot = find_guard_slot(updated_day, updated_hour, spot_name, days)
                if slot and self in watch_list[slot['start']['day']][slot['start']['hour']][spot_name]:
                    return False

        return True


def get_days_list(start_day, end_day):
    days_list = list()
    days_cycle = cycle(week_days)

    w_d = next(days_cycle)
    while w_d != start_day:
        w_d = next(days_cycle)

    days_list.append(w_d)

    while w_d != end_day:
        w_d = next(days_cycle)
        days_list.append(w_d)

    return days_list


def get_hours_list(day, start_day, end_day, start_hour, end_hour):
    hours_list = list()
    days_list = get_days_list(start_day, end_day)

    for hour in range(24):
        if day == start_day and hour >= start_hour:
            hours_list.append(hour)

        elif day in days_list and day != start_day and day != end_day:
            hours_list.append(hour)

        elif day == end_day and hour < end_hour:
            hours_list.append(hour)

    return hours_list
