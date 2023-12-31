# Copyright (c) 2023, Andy Benichou
# All rights reserved.
#
# This file is part of a software project governed by the Custom License
# for Private Use.
# Redistribution and use in source and binary forms, with or
# without modification, are not permitted for any non-commercial or
# commercial purposes without prior written permission from the owner.
#
# This software is provided "as is", without warranty of any kind,
# express or implied.
# In no event shall the authors be liable for any claim, damages,
# or other liability.
#
# For full license terms, see the LICENSE file in the project root
# or contact Andy Benichou.
#
# Guard file of the project Meshavshek


from datetime import datetime, timedelta
from copy import deepcopy

from config import MINIMAL_DELAY, PARTNER_MINIMAL_DELAY
from src.models.Spot import Spot


class Guard:
    def __init__(self, first_name, last_name,
                 partner=None, same_time_partners=None,
                 not_partners=None,
                 not_available_times=None,
                 is_guarding=True, is_living_far_away=False,
                 spots_preferences=None, time_preferences=None,
                 last_spot=None, room=None):
        self.first_name = first_name
        self.last_name = last_name
        self.partner = partner
        self.same_time_partners = same_time_partners if same_time_partners else list()
        self.not_partners = not_partners if not_partners else list()
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
        new_guard = Guard(first_name=self.first_name,
                          last_name=self.last_name,
                          partner=self.partner,
                          same_time_partners=None,
                          not_partners=None,
                          is_guarding=self.is_guarding,
                          is_living_far_away=self.is_living_far_away,
                          spots_preferences=None,
                          time_preferences=None,
                          last_spot=self.last_spot,
                          room=None)

        # Add the new instance to the memo dictionary to avoid recursive loops
        memo = memo or {}
        memo[id(self)] = new_guard

        # Now manually deepcopy the deep attributes without passing the memo dictionary
        new_guard.not_available_times = deepcopy(self.not_available_times, memo)
        new_guard.time_preferences = deepcopy(self.time_preferences, memo)
        new_guard.same_time_partners = deepcopy(self.same_time_partners, memo)
        new_guard.not_partners = deepcopy(self.not_partners, memo)
        new_guard.spots_preferences = deepcopy(self.spots_preferences, memo)
        new_guard.room = deepcopy(self.room, memo)

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

    def is_missing_during_spot(self, spot, date):
        if spot:
            guard_slot = spot.find_guard_slot(date)
            if guard_slot:
                for missing_times in self.not_available_times:
                    # Leaves before the beginning
                    if missing_times['start'] <= guard_slot['start']:
                        # Comes back after the beginning
                        if missing_times['end'] > guard_slot['start']:
                            return True

                    # Leaves after the beginning
                    if missing_times['start'] >= guard_slot['start']:
                        # But before the end
                        if missing_times['start'] < guard_slot['end']:
                            return True
        return False

    def in_time_preferences(self, date: datetime, spot=None):
        if self.time_preferences:
            in_time_preferences = False

            if spot:
                guard_slot = spot.find_guard_slot(date)
                if guard_slot:
                    for time_pref in self.time_preferences:
                        start, end = date.replace(hour=time_pref['start']), date.replace(hour=time_pref['end'])
                        if start <= guard_slot['start'] \
                                and end >= guard_slot['end']:
                            in_time_preferences = True

            else:
                for time_pref in self.time_preferences:
                    if time_pref['start'] <= date.hour < time_pref['end']:
                        in_time_preferences = True

            if not in_time_preferences:
                return False

        return True

    # Helper function to check if a guard is available
    def is_available(self, watch_list, date, spot: Spot = None,
                     delays_prop=None,
                     break_no_same_consecutive_spot_rule=False,
                     not_missing_delay=0, curr_guards=None,
                     next_guards_to_place_when_available=None):

        if not self.is_guarding:
            return False

        if spot and self.spots_preferences \
                and spot not in self.spots_preferences:
            return False

        for h in range(0, not_missing_delay + 1):
            new_date = date + timedelta(hours=h)
            if self.is_missing(new_date):
                if next_guards_to_place_when_available:
                    next_guards_to_place_when_available.append(self)
                return False

        if self.is_missing_during_spot(spot, date):
            return False

        if spot and self.last_spot == spot and not \
                (self.last_spot in self.spots_preferences and
                 len(self.spots_preferences) == 1) \
                and not break_no_same_consecutive_spot_rule:
            return False

        if not self.in_time_preferences(date, spot):
            if next_guards_to_place_when_available:
                next_guards_to_place_when_available.append(self)
            return False

        if curr_guards:
            for g in curr_guards:
                if g in self.not_partners or self in g.not_partners:
                    return False

        for rest_delay in (delays_prop if delays_prop else list(range(0, MINIMAL_DELAY + 1))):
            updated_date = date - timedelta(hours=rest_delay)

            if updated_date not in watch_list:
                continue

            # Check if the guard already in another spot
            for spot_obj in watch_list[updated_date]:
                if self in watch_list[updated_date][spot_obj]:
                    return False

        return True

    def is_partner_available(self, guards_list, watch_list, date, spot,
                             break_no_same_consecutive_spot_rule=False):
        if not self.partner:
            return True

        return guards_list.find(self.partner).is_available(watch_list, date,
                                                           spot=spot,
                                                           delays_prop=list(range(0,
                                                                                  min(PARTNER_MINIMAL_DELAY, MINIMAL_DELAY) + 1, 3)),
                                                           break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule)
