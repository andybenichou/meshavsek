import random

from collections import defaultdict
from copy import deepcopy
from itertools import cycle

from GuardsList import GuardsList
from consts import TRIES_NUMBER, WEEK_DAYS, MINIMAL_DELAY, \
    RANDOMNESS_LEVEL, PREVIOUS_FILE_NAME, MISSING_GUARDS_FILE_NAME, GUARD_SPOTS
from export import export_to_excel
from get_previous_data import get_previous_data
from get_missing_guards import get_missing_guards
from helper import get_today_day_of_week, find_guard_slot

from guards_properties import GUARDS_LIST


class MaxIterationsReached(Exception):
    def __init__(self, message="Maximum iterations reached in the function"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class ImpossibleToFillPlanning(Exception):
    def __init__(self, message="Impossible to fill planning"):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


def print_delays(bad_delays, too_good_delays):
    # Map each day to its numeric value
    day_to_num = {day: num for num, day in enumerate(WEEK_DAYS)}

    # Sort the data
    bad_delays = sorted(bad_delays, key=lambda x: (day_to_num[x['start']['day']], x['start']['hour']))
    too_good_delays = sorted(too_good_delays, key=lambda x: (day_to_num[x['start']['day']], x['start']['hour']))

    if bad_delays or too_good_delays:
        print()

    for b_d in bad_delays:
        print(
            f'{b_d["guard"]} יש לו רק {b_d["delay"]} שעות מנוחה לפני המשמרת ביום {b_d["start"]["day"]} בשעה {b_d["start"]["hour"]}')

    if bad_delays:
        print()

    for g_d in too_good_delays:
        print(
            f'{g_d["guard"]} יש לו {g_d["delay"]} שעות מנוחה לפני המשמרת ביום {g_d["start"]["day"]} בשעה {g_d["start"]["hour"]}')


def get_guards_slots(watch_list, days, guards):
    guard_slots = {guard.name: list() for guard in guards}

    for guard in guards:
        for day in watch_list:
            for hour in watch_list[day]:
                for spot in watch_list[day][hour]:
                    if guard in watch_list[day][hour][spot]:
                        slot = find_guard_slot(day, hour, spot, days)

                        if slot and slot not in guard_slots[guard.name]:
                            guard_slots[guard.name].append(slot)

    return guard_slots


def check_guards_slots_delays(watch_list, days, guards, need_print=False):
    guard_slots = get_guards_slots(watch_list, days, guards)
    bad_delays = list()
    too_good_delays = list()

    for guard in guard_slots:
        last_slot = None
        for slot in guard_slots[guard]:
            start_day, start_hour = slot['start']['day'], slot['start']['hour']

            if last_slot:
                days_cycle = cycle(days)
                curr_day = next(days_cycle)
                while curr_day != last_slot['end']['day']:
                    curr_day = next(days_cycle)

                while curr_day != start_day:
                    curr_day = next(days_cycle)
                    start_hour += 24

                delay = start_hour - last_slot['end']['hour']

                if delay <= MINIMAL_DELAY:
                    bad_delays.append({
                        'guard': guard,
                        'delay': delay,
                        'start': slot['start'],
                    })
                elif MINIMAL_DELAY + 3 < delay <= MINIMAL_DELAY + 12:
                    too_good_delays.append({
                        'guard': guard,
                        'delay': delay,
                        'start': slot['start'],
                    })

            last_slot = slot

    if need_print:
        print_delays(bad_delays, too_good_delays)

    return len(bad_delays)


# Align guards cycle to the next available guard
def align_guards_cycle(watch_list, guard_cycle_prop,
                       guards_list_prop: GuardsList,
                       day, hour, days,
                       currently_missing_guards):
    guard = guards_list_prop.get_current_guard()

    if not guard:
        guard = next(guard_cycle_prop)
        guards_list_prop.set_current_guard(guard)

    while not guard.is_available(watch_list, day, hour, days):
        if guard.is_missing(day, hour):
            currently_missing_guards.append(guard)

        guard = next(guard_cycle_prop)
        guards_list_prop.set_current_guard(guard)

    return guard


def get_random_guards(watch_list, buff_cycle, currently_missing_guards,
                      day, hour, spot, days, guards):
    random_guards = list()
    while len(random_guards) != RANDOMNESS_LEVEL:
        guard = None
        for g in currently_missing_guards:
            if g.is_available(watch_list, day, hour, days,
                              spot=spot):
                guard = g
                currently_missing_guards.remove(g)
                break

        if not guard:
            guard = next(buff_cycle)

        if guard.is_available(watch_list, day, hour, days, spot=spot) \
                and guard not in guards:
            random_guards.append(guard)

    random.shuffle(random_guards)
    return random_guards


# Helper function to get the next available guard
def get_next_available_guard(guards_list_prop: GuardsList,
                             watch_list, guard_cycle_prop, day, hour,
                             days, currently_missing_guards,
                             spot, guards: GuardsList = None, no_duo=False):
    hopel = guards_list_prop.find('משה החופל')

    if hour == 5 and hopel \
            and hopel.is_available(watch_list, day, hour, days) \
            and hopel not in guards:
        return hopel, None

    curr_guard = align_guards_cycle(watch_list, guard_cycle_prop,
                                    guards_list_prop,
                                    day, hour, days,
                                    currently_missing_guards)

    index = guards_list_prop.index(curr_guard)
    buff_cycle = cycle(guards_list_prop[index:] + guards_list_prop[:index])

    MAX_ITERATIONS = 1000  # Set a maximum limit for the number of iterations
    iteration_count = 0
    while True:
        if iteration_count > MAX_ITERATIONS:
            raise MaxIterationsReached

        iteration_count += 1

        random_guards = get_random_guards(watch_list, buff_cycle,
                                          currently_missing_guards,
                                          day, hour, spot, days,
                                          guards)

        for guard in random_guards:
            partner = guards_list_prop.find(guard.partner)
            if partner:
                if not partner.is_available(watch_list, day, hour,
                                            days, delays_prop=[0, 3, 6]):
                    return guard, None

                if partner.spots_preferences \
                        and spot not in partner.spots_preferences:
                    continue

                if no_duo:
                    continue

                return guard, partner

            else:
                return guard, None


def get_already_filled_guard_slot(watch_list, day, hour, spot, days):
    guards = watch_list[day][hour][spot] if watch_list[day][hour][spot] else list()
    fill_guard_spot = False

    # Spot already filled
    if len(guards) == GUARD_SPOTS[spot]['guards_number']:
        return guards, fill_guard_spot

    # Fill the actual hour with the slot guards if there are already in one of
    # the slot
    slot = find_guard_slot(day, hour, spot, days)

    if slot:
        guards = watch_list[slot['start']['day']][slot['start']['hour']][spot]

        if len(guards) != GUARD_SPOTS[spot]['guards_number']:
            fill_guard_spot = True

    return guards, fill_guard_spot


def get_guards(guards_list_prop: GuardsList, watch_list, guard_cycle, day,
               hour, spot, days, currently_missing_guards):
    guards, fill_guard_spot = \
        get_already_filled_guard_slot(watch_list, day, hour, spot, days)

    guards = GuardsList(guards)

    if len(guards) == GUARD_SPOTS[spot]['guards_number']:
        return guards

    if fill_guard_spot:
        guard1, guard2 = get_next_available_guard(guards_list_prop,
                                                  watch_list,
                                                  guard_cycle,
                                                  day,
                                                  hour,
                                                  days,
                                                  currently_missing_guards,
                                                  spot,
                                                  guards=guards)

        for g in [guard1, guard2]:
            if len(guards) != GUARD_SPOTS[spot]['guards_number'] and g:
                guards.append(g)

        if len(guards) == 1 and GUARD_SPOTS[spot]['guards_number'] == 2:
            guard2 = get_next_available_guard(guards_list_prop,
                                              watch_list,
                                              guard_cycle,
                                              day,
                                              hour,
                                              days,
                                              currently_missing_guards,
                                              spot,
                                              guards=guards,
                                              no_duo=True)[0]
            guards.append(guard2)
        guards.sort()

    return guards


def get_watch_list_data(guards_list_prop: GuardsList, watch_list, days,
                        first_hour_prop):
    currently_missing_guards = GuardsList()

    # Assign guards to each slot
    guard_cycle = cycle(guards_list_prop)
    for day in days:
        for hour in range(24):
            if day == days[0] and hour < first_hour_prop:
                continue

            # Remove unnecessary start and end of planning
            if (days.index(day) == 0 and hour < 2) or \
                    (days.index(day) == len(days) - 1
                     and hour >= 20):
                continue

            spots = list(GUARD_SPOTS.keys())
            random.shuffle(spots)
            for spot in spots:
                guards = get_guards(guards_list_prop, watch_list, guard_cycle,
                                    day, hour, spot, days,
                                    currently_missing_guards)

                if len(guards) == GUARD_SPOTS[spot]['guards_number'] \
                        and not watch_list[day][hour][spot]:
                    for g in guards:
                        g.last_spot = spot
                    watch_list[day][hour][spot].extend(guards)

    return watch_list


def get_first_hour(watch_list, days):
    # Get first hour of first day:
    first_hour = None
    for d in days:
        for h in range(24):
            if h in watch_list[d].keys() and not first_hour:
                return h

    return 2


def get_days(watch_list, days_input=None):
    if not days_input:
        days_input = input("How many days do you need to schedule? ") \

    while True:
        if days_input.isdigit():
            days_num = int(days_input)
            break
        else:
            days_input = input("Please enter a valid integer. ")

    days = list(
        watch_list.keys()) if watch_list.keys() else [get_today_day_of_week()]
    days_cycle = cycle(WEEK_DAYS)

    day = next(days_cycle)
    while days[-1] != day:
        day = next(days_cycle)

    for _ in range(days_num):
        day = next(days_cycle)

        if day in days:
            break

        # Initialize day in watch_list
        watch_list[day] = defaultdict(lambda: defaultdict(GuardsList))
        days.append(day)

    first_hour = get_first_hour(watch_list, days)

    return days, days_input, first_hour


def init_watch_list(guards, print_missing_names):
    # Initialize the watch list
    watch_list = defaultdict(lambda: defaultdict(lambda: defaultdict(GuardsList)))

    watch_list = get_previous_data(PREVIOUS_FILE_NAME, watch_list, guards,
                                   GUARD_SPOTS, print_missing_names=print_missing_names)

    missing_guards = get_missing_guards(MISSING_GUARDS_FILE_NAME, guards)

    return watch_list, missing_guards


def plan(user_input_prop, guards, print_missing_names, retry_after_infinite_loop_num=0):
    watch_list, _ = init_watch_list(guards, print_missing_names)
    days, user_i, first_hour = get_days(watch_list, days_input=user_input_prop)

    try:
        if retry_after_infinite_loop_num >= 20:
            raise ImpossibleToFillPlanning("Watch list can't be filled with this context, "
                                           "try to recruit more guards, remove some guard spots "
                                           "or reduce the MINIMAL_DELAY between each guard in consts file")

        watch_list = get_watch_list_data(guards, watch_list, days, first_hour)
        delays_num = check_guards_slots_delays(watch_list, days, guards)

    except MaxIterationsReached:
        print("Maximum number of iterations reached, retrying...")
        return plan(user_i, guards, print_missing_names,
                    retry_after_infinite_loop_num=retry_after_infinite_loop_num + 1)

    return user_i, days, delays_num, watch_list


if __name__ == '__main__':
    try_num = 0
    min_delays = 0
    best_wl = None
    user_input = None
    days_list = list()
    guards_list = None
    while try_num < TRIES_NUMBER:
        guards_list = deepcopy(GUARDS_LIST)
        user_input, days_list, delays, wl = plan(user_input, guards_list,
                                                 try_num == 0)

        if not min_delays or delays < min_delays:
            min_delays = delays
            best_wl = wl

        try_num += 1

        print(f'Try {try_num}')

        if user_input == '0':
            break

    export_to_excel('watch_list', best_wl, days_list, GUARD_SPOTS)
    check_guards_slots_delays(best_wl, days_list, guards_list,
                              need_print=True)

    print('\nShivsakta!')
