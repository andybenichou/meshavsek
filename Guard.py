from copy import deepcopy
from itertools import cycle

from consts import MINIMAL_DELAY, WEEK_DAYS, GUARD_SPOTS
from helper import get_prec_day, find_guard_slot


class Guard:
    def __init__(self, first_name, last_name,
                 partner=None, same_time_partners=None,
                 not_available_times=None,
                 is_guarding=True, is_living_far_away=False,
                 spots_preferences=None, time_preferences=None,
                 last_spot=None, room=None):
        self.first_name = first_name
        self.last_name = last_name
        self.partner = partner
        self.same_time_partners = same_time_partners if same_time_partners else list()
        self.__not_available_times = not_available_times \
            if not_available_times else list()
        self.is_guarding = is_guarding
        self.is_living_far_away = is_living_far_away
        self.spots_preferences = spots_preferences
        self.time_preferences = time_preferences
        self.last_spot = last_spot
        self.room = room

    def __repr__(self):
        return f"Guard(first_name={self.first_name!r}, last_name={self.last_name!r})"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def __eq__(self, other):
        if isinstance(other, Guard):
            return (self.first_name == other.first_name and self.last_name == other.last_name) \
                or (self.first_name == other.last_name and self.last_name == other.first_name)

        elif isinstance(other, str):
            return self.first_name in other and self.last_name in other

        return False

    def __deepcopy__(self, memo=None):
        # Create a new instance with 'None' for deep attributes initially to avoid recursive deepcopy calls
        new_guard = Guard(self.first_name, self.last_name, self.partner,
                          None, None, self.is_guarding, self.is_living_far_away,
                          None, None, self.last_spot)

        # Add the new instance to the memo dictionary to avoid recursive loops
        memo = memo or {}
        memo[id(self)] = new_guard

        # Now manually deepcopy the deep attributes without passing the memo dictionary
        new_guard.__not_available_times = deepcopy(self.__not_available_times, memo)
        new_guard.time_preferences = deepcopy(self.time_preferences, memo)
        new_guard.same_time_partners = deepcopy(self.same_time_partners, memo)
        new_guard.spots_preferences = deepcopy(self.spots_preferences, memo)

        return new_guard

    def add_not_available_time(self, start, end):
        time_obj = {
            'start': start,
            'end': end
        }

        for not_available_time in self.__not_available_times:
            delete_not_available_time = False
            # Starts before the beginning
            if (time_obj['start']['day'] == not_available_time['start']['day'] and
                    time_obj['start']['hour'] <= not_available_time['start']['hour']) \
                    or time_obj['start']['day'] < not_available_time['start']['day']:
                # Finishes after the beginning
                if (time_obj['end']['day'] == not_available_time['start']['day'] and
                        time_obj['end']['hour'] >= not_available_time['start']['hour']) \
                        or time_obj['end']['day'] > not_available_time['start']['day']:
                    # But before the end
                    if (time_obj['end']['day'] == not_available_time['end']['day'] and
                            time_obj['end']['hour'] <= not_available_time['end']['hour']) \
                            or time_obj['end']['day'] < not_available_time['end']['day']:
                        time_obj['end'] = not_available_time['end']
                        delete_not_available_time = True

            # Starts after the beginning
            if (time_obj['start']['day'] == not_available_time['start']['day'] and
                time_obj['start']['hour'] >= not_available_time['start']['hour']) \
                    or time_obj['start']['day'] > not_available_time['start']['day']:
                # But before the end
                if (time_obj['start']['day'] == not_available_time['end']['day'] and
                    time_obj['start']['hour'] <= not_available_time['end']['hour']) \
                        or time_obj['start']['day'] < not_available_time['end']['day']:
                    # Finishes after the end
                    if (time_obj['end']['day'] == not_available_time['end']['day'] and
                        time_obj['end']['hour'] >= not_available_time['end']['hour']) \
                            or time_obj['end']['day'] > not_available_time['end']['day']:
                        time_obj['start'] = not_available_time['start']
                        delete_not_available_time = True

            if delete_not_available_time:
                self.__not_available_times.remove(not_available_time)

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
        def is_missing_during_spot():
            def day_is_before(first, second):
                return completed_days.index(first) < completed_days.index(second)

            completed_days = days + [d for d in WEEK_DAYS if d not in days]

            if spot:
                guard_slot = find_guard_slot(day, hour, spot, WEEK_DAYS + WEEK_DAYS)
                if guard_slot:
                    for missing_times in self.__not_available_times:
                        # Leaves before the beginning
                        if (missing_times['start']['day'] == guard_slot['start']['day'] and
                            missing_times['start']['hour'] <= guard_slot['start']['hour']) \
                                or day_is_before(missing_times['start']['day'], guard_slot['start']['day']):
                            # Comes back after the beginning
                            if (missing_times['end']['day'] == guard_slot['start']['day'] and
                                missing_times['end']['hour'] >= guard_slot['start']['hour']) \
                                    or day_is_before(guard_slot['start']['day'], missing_times['end']['day']):
                                return True

                        # Leaves after the beginning
                        if (missing_times['start']['day'] == guard_slot['start']['day'] and
                            missing_times['start']['hour'] >= guard_slot['start']['hour']) \
                                or day_is_before(guard_slot['start']['day'], missing_times['start']['day']):
                            # But before the end
                            if (missing_times['start']['day'] == guard_slot['end']['day'] and
                                missing_times['start']['hour'] <= guard_slot['end']['hour']) \
                                    or day_is_before(missing_times['start']['day'], guard_slot['end']['day']):
                                return True
            return False

        if not self.is_guarding:
            return False

        if spot and self.spots_preferences \
                and spot not in self.spots_preferences:
            return False

        if self.is_missing(day, hour):
            return False

        if is_missing_during_spot():
            return False

        if spot and self.last_spot == spot:
            return False

        if self.time_preferences:
            in_time_preferences = False
            for time_pref in self.time_preferences:
                if time_pref['start'] <= hour < time_pref['end']:
                    in_time_preferences = True

            if not in_time_preferences:
                return False

        for rest_delay in (delays_prop if delays_prop else list(range(0, MINIMAL_DELAY + 1, 3))):
            updated_hour = hour - rest_delay
            updated_day = day

            if updated_hour < 0:
                updated_day = get_prec_day(day, days)
                updated_hour += 24

            if not updated_day:
                break

            # Check if the guard already in another spot
            for spot_name in GUARD_SPOTS:
                slot = find_guard_slot(updated_day, updated_hour, spot_name, days)
                if slot and self in watch_list[slot['start']['day']][slot['start']['hour']][spot_name]:
                    return False

        return True

    def is_partner_available(self, guards_list, watch_list, day, hour, days, spot):
        if not self.partner:
            return True

        return guards_list.find(self.partner).is_available(watch_list, day, hour,
                                                           days, spot=spot,
                                                           delays_prop=[0, 3, 6])


def get_days_list(start_day, end_day):
    days_list = list()
    days_cycle = cycle(WEEK_DAYS)

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
