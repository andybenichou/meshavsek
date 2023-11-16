from datetime import datetime, timedelta
from copy import deepcopy

from consts import MINIMAL_DELAY, GUARD_SPOTS, PARTNER_MINIMAL_DELAY
from helper import find_guard_slot


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
        self.not_available_times = not_available_times \
            if not_available_times else list()
        self.is_guarding = is_guarding
        self.is_living_far_away = is_living_far_away
        self.spots_preferences = spots_preferences \
            if spots_preferences else list()
        self.time_preferences = time_preferences \
            if time_preferences else list()
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
        new_guard.not_available_times = deepcopy(self.not_available_times, memo)
        new_guard.time_preferences = deepcopy(self.time_preferences, memo)
        new_guard.same_time_partners = deepcopy(self.same_time_partners, memo)
        new_guard.spots_preferences = deepcopy(self.spots_preferences, memo)

        return new_guard

    def add_not_available_time(self, start: datetime, end: datetime):
        time_obj = {
            'start': start,
            'end': end
        }

        for not_available_time in self.not_available_times:
            delete_not_available_time = False
            # Starts before the beginning
            if time_obj['start'] <= not_available_time['start']:
                # Finishes after the beginning
                if time_obj['end'] >= not_available_time['start']:
                    # But before the end
                    if time_obj['end'] <= not_available_time['end']:
                        time_obj['end'] = not_available_time['end']
                        delete_not_available_time = True

            # Starts after the beginning
            if time_obj['start'] >= not_available_time['start']:
                # But before the end
                if time_obj['start'] <= not_available_time['end']:
                    # Finishes after the end
                    if time_obj['end'] >= not_available_time['end']:
                        time_obj['start'] = not_available_time['start']
                        delete_not_available_time = True

            if delete_not_available_time:
                self.not_available_times.remove(not_available_time)

        if time_obj not in self.not_available_times:
            self.not_available_times.append(time_obj)

    def is_missing(self, date: datetime):
        for not_available_time in self.not_available_times:
            if not_available_time['start'] <= date < not_available_time['end']:
                return True
        return False

    def in_time_preferences(self, date: datetime):
        if self.time_preferences:
            in_time_preferences = False
            for time_pref in self.time_preferences:
                if time_pref['start'] <= date.hour < time_pref['end']:
                    in_time_preferences = True

            if not in_time_preferences:
                return False

        return True

    # Helper function to check if a guard is available
    def is_available(self, watch_list, date, spot=None,
                     delays_prop=None,
                     break_no_same_consecutive_spot_rule=False,
                     not_missing_delay=0):
        def is_missing_during_spot():
            if spot:
                guard_slot = find_guard_slot(GUARD_SPOTS, date, spot)
                if guard_slot:
                    for missing_times in self.not_available_times:
                        # Leaves before the beginning
                        if missing_times['start'] <= guard_slot['start']:
                            # Comes back after the beginning
                            if missing_times['end'] >= guard_slot['start']:
                                return True

                        # Leaves after the beginning
                        if missing_times['start'] >= guard_slot['start']:
                            # But before the end
                            if missing_times['start'] <= guard_slot['end']:
                                return True
            return False

        if not self.is_guarding:
            return False

        if spot and self.spots_preferences \
                and spot not in self.spots_preferences:
            return False

        for h in range(0, not_missing_delay + 1):
            new_date = date + timedelta(hours=h)
            if self.is_missing(new_date):
                return False

        if is_missing_during_spot():
            return False

        if spot and self.last_spot == spot and not \
                (self.last_spot in self.spots_preferences and
                 len(self.spots_preferences) == 1) \
                and not break_no_same_consecutive_spot_rule:
            return False

        if not self.in_time_preferences(date):
            return False

        for rest_delay in (delays_prop if delays_prop else list(range(0, MINIMAL_DELAY + 1))):
            updated_date = date - timedelta(hours=rest_delay)

            if updated_date not in watch_list:
                continue

            # Check if the guard already in another spot
            for spot_name in watch_list[updated_date]:
                if self in watch_list[updated_date][spot_name]:
                    return False

        return True

    def is_partner_available(self, guards_list, watch_list, date, spot,
                             break_no_same_consecutive_spot_rule=False):
        if not self.partner:
            return True

        return guards_list.find(self.partner).is_available(watch_list, date,
                                                           spot=spot,
                                                           delays_prop=list(range(0, PARTNER_MINIMAL_DELAY + 1, 3)),
                                                           break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule)
