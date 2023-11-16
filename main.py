import random

from collections import defaultdict
from copy import deepcopy
from datetime import datetime, timedelta
from itertools import cycle

from GuardsList import GuardsList
from Room import Room
from consts import TRIES_NUMBER, MINIMAL_DELAY, \
    RANDOMNESS_LEVEL, PREVIOUS_FILE_NAME, MISSING_GUARDS_FILE_NAME, \
    GUARD_SPOTS, NEW_WATCH_LIST_FILE_NAME, FIRST_HOUR_FIRST_DATE, \
    LAST_HOUR_LAST_DATE, RETRIES_NUM_BEFORE_CRASH, KITAT_KONENOUT_DURATION, \
    MINIMUM_AVAILABLE_SOLDIERS_KITAT_CONENOUT, MISSING_GUARDS_SHEET_NAME, \
    PARTNER_MINIMAL_DELAY, TORANOUT_PROPS
from export import export_to_excel
from get_available_guards_per_date import get_available_guards_per_date
from get_previous_data import get_previous_data
from get_missing_guards import get_missing_guards
from helper import find_guard_slot, get_day_at_midnight, get_day_of_week, \
    sort_watch_list

from guards_properties import GUARDS_LIST, ROOMS_LIST


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
    def print_delay(delay_obj, good=False):
        guard = delay_obj['guard']
        delay = delay_obj['delay']
        day = delay_obj['start'].day
        month = delay_obj['start'].month
        hour = delay_obj['start'].hour
        week_day = get_day_of_week(delay_obj["start"])
        if good:
            print(
                f'{guard} יש לו {delay} שעות מנוחה לפני המשמרת ביום {week_day} - {day}.{month} - {hour}:00')
        else:
            print(
                f'{guard} יש לו רק {delay} שעות מנוחה לפני המשמרת ביום {week_day} - {day}.{month} - {hour}:00')

    # Sort the data
    bad_delays = sorted(bad_delays, key=lambda x: x['start'])
    too_good_delays = sorted(too_good_delays, key=lambda x: x['start'])

    if bad_delays:
        print()
        print('Bad delays:')

    for bad_delay in bad_delays:
        print_delay(bad_delay, good=False)

    if too_good_delays:
        print()
        print('Good delays:')

    for good_delay in too_good_delays:
        print_delay(good_delay, good=True)


def get_guards_slots(watch_list, guards):
    guard_slots = {str(guard): list() for guard in guards}

    for guard in guards:
        for date in watch_list:
            for spot in GUARD_SPOTS:
                if guard in watch_list[date][spot]:
                    slot = find_guard_slot(GUARD_SPOTS, date, spot)
                    if slot and slot not in guard_slots[str(guard)]:
                        guard_slots[str(guard)].append(slot)

    return guard_slots


def check_guards_slots_delays(watch_list, guards, need_print=False):
    guards_slots = get_guards_slots(watch_list, guards)
    bad_delays = list()
    too_good_delays = list()

    for guard in guards_slots:
        last_slot = None
        for slot in guards_slots[guard]:
            if last_slot:
                time_diff = slot['start'] - last_slot['end']
                delay = time_diff.days * 24 + time_diff.seconds // 3600

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


def get_num_guards_available(watch_list, guards_list_prop, date, spot=None,
                             chosen_guards=None):
    available_num = 0
    for g in guards_list_prop:
        if g.is_available(watch_list, date, spot=spot) \
                and ((chosen_guards and g not in chosen_guards) or not chosen_guards):
            available_num += 1

    return available_num


def get_num_no_partner_guards_available(watch_list, guards_list_prop, date,
                                        spot=None, chosen_guards=None):
    no_partner_available_num = 0
    for g in guards_list_prop:
        if g.is_available(watch_list, date, spot=spot) \
                and (not g.partner
                     or not g.is_partner_available(guards_list_prop,
                                                   watch_list, date,
                                                   spot)) \
                and ((chosen_guards and g not in chosen_guards) or not chosen_guards):
            no_partner_available_num += 1

    return no_partner_available_num


def need_break_no_same_consecutive_spot_rule(watch_list, guards_list_prop,
                                             date, get_num_guards_available_fun,
                                             spot, chosen_guards=None):
    available_guards_num_no_same_spot = get_num_guards_available_fun(watch_list,
                                                                     guards_list_prop,
                                                                     date,
                                                                     spot=spot,
                                                                     chosen_guards=chosen_guards)
    available_guards_num_total = get_num_guards_available_fun(watch_list,
                                                              guards_list_prop,
                                                              date,
                                                              chosen_guards=chosen_guards)

    break_no_same_consecutive_spot_rule = available_guards_num_total > 0 and available_guards_num_no_same_spot == 0

    available_guards_num = available_guards_num_no_same_spot if not break_no_same_consecutive_spot_rule \
        else available_guards_num_total

    spot = spot if not break_no_same_consecutive_spot_rule else None

    return break_no_same_consecutive_spot_rule, available_guards_num, spot


def get_random_guards(watch_list, guards_list_prop, buff_cycle,
                      same_time_partners, next_guards_to_place_when_available,
                      date, spot, guards, no_duo):
    if no_duo:
        break_no_same_consecutive_spot_rule, available_guards_num, spot = \
            need_break_no_same_consecutive_spot_rule(watch_list, guards_list_prop,
                                                     date,
                                                     get_num_no_partner_guards_available,
                                                     spot=spot, chosen_guards=guards)
    else:
        break_no_same_consecutive_spot_rule, available_guards_num, spot = \
            need_break_no_same_consecutive_spot_rule(watch_list, guards_list_prop,
                                                     date,
                                                     get_num_guards_available,
                                                     spot, chosen_guards=guards)

    if available_guards_num <= 0:
        raise MaxIterationsReached

    random_guards = list()
    break_while = False
    while len(random_guards) != RANDOMNESS_LEVEL:
        if len(random_guards) == available_guards_num:
            break

        guard = None
        for g in same_time_partners:
            if g.is_available(watch_list, date, spot=spot,
                              break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule):
                guard = g
                same_time_partners.remove(g)

                if g in next_guards_to_place_when_available:
                    next_guards_to_place_when_available.remove(g)
                break_while = True
                break

        if not guard:
            for g in next_guards_to_place_when_available:
                if g.is_available(watch_list, date, spot=spot,
                                  break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule):
                    guard = g
                    next_guards_to_place_when_available.remove(g)
                    break_while = True
                    break

        if not guard:
            guard = next(buff_cycle)

        if guard.is_available(watch_list, date, spot=spot) \
                and guard not in guards and guard not in random_guards:
            if no_duo and guard.partner and \
                guard.is_partner_available(guards_list_prop, watch_list,
                                           date, spot,
                                           break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule):
                continue
            random_guards.append(guard)

        if break_while:
            break

    random.shuffle(random_guards)
    return random_guards


# Align guards cycle to the next available guard
def get_curr_guard_available(watch_list, guards_list_prop: GuardsList,
                             date, next_guards_to_place_when_available):
    guards_cycle = cycle(guards_list_prop)
    guard = next(guards_cycle)

    if guards_list_prop.get_current_guard():
        while guard != guards_list_prop.get_current_guard():
            guard = next(guards_cycle)
    else:
        guards_list_prop.set_current_guard(guard)

    first_guard = guard
    while not guard.is_available(watch_list, date):
        if guard.is_missing(date) or not guard.in_time_preferences(date):
            next_guards_to_place_when_available.append(guard)

        guard = next(guards_cycle)
        guards_list_prop.set_current_guard(guard)

        if guard == first_guard:
            raise MaxIterationsReached

    return guard


# Helper function to get the next available guard
def get_next_available_guard(guards_list_prop: GuardsList,
                             watch_list, date,
                             next_guards_to_place_when_available, same_time_partners,
                             spot, break_partners: bool,
                             guards: GuardsList = None, no_duo=False):
    no_partner_available_guards = get_num_guards_available(watch_list, guards_list_prop, date, chosen_guards=guards)

    break_partners = break_partners and (no_partner_available_guards - len(guards) <= 0)

    curr_guard = get_curr_guard_available(watch_list, guards_list_prop, date,
                                          next_guards_to_place_when_available)
    index = guards_list_prop.index(curr_guard)
    buff_cycle = cycle(guards_list_prop[index:] + guards_list_prop[:index])

    break_no_same_consecutive_spot_rule, available_guards_num, spot = \
        need_break_no_same_consecutive_spot_rule(watch_list, guards_list_prop,
                                                 date,
                                                 get_num_guards_available,
                                                 spot, chosen_guards=guards)

    if available_guards_num == 0:
        raise MaxIterationsReached

    chosen_guards = None
    while True:
        random_guards = get_random_guards(watch_list, guards_list_prop,
                                          buff_cycle, same_time_partners,
                                          next_guards_to_place_when_available,
                                          date, spot, guards,
                                          no_duo=no_duo and not break_partners)

        for guard in random_guards:
            partner = guards_list_prop.find(guard.partner)
            if partner:
                if not guard.is_partner_available(guards_list_prop,
                                                  watch_list, date, spot,
                                                  break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule):
                    chosen_guards = (guard, None)
                    break

                elif partner.spots_preferences \
                        and spot not in partner.spots_preferences:
                    continue

                elif no_duo and not break_partners:
                    continue

                elif no_duo and break_partners:
                    chosen_guards = (guard, None)
                    break

                else:
                    chosen_guards = (guard, partner)
                    break

            else:
                chosen_guards = (guard, None)
                break

        if chosen_guards:
            for g in chosen_guards:
                if not g:
                    continue

                for partner in g.same_time_partners:
                    if partner not in same_time_partners:
                        partner = guards_list_prop.find(partner)
                        if partner.is_available(watch_list, date,
                                                spot=spot,
                                                delays_prop=list(range(0, PARTNER_MINIMAL_DELAY + 1, 3)),
                                                break_no_same_consecutive_spot_rule=break_no_same_consecutive_spot_rule):
                            same_time_partners.append(partner)
            return chosen_guards


def get_already_filled_guard_slot(watch_list, date, spot):
    guards = watch_list[date][spot] if watch_list[date][spot] else list()
    fill_guard_spot = False

    # Spot already filled
    if len(guards) == GUARD_SPOTS[spot]['guards_number']:
        return guards, fill_guard_spot

    # Fill the actual hour with the slot guards if there are already in one of
    # the slot
    slot = find_guard_slot(GUARD_SPOTS, date, spot)

    if slot:
        guards = watch_list[slot['start']][spot]

        if len(guards) != GUARD_SPOTS[spot]['guards_number']:
            fill_guard_spot = True

    return guards, fill_guard_spot


def get_guards(guards_list_prop: GuardsList, watch_list, date, spot,
               next_guards_to_place_when_available, same_time_partners,
               break_partners: bool):
    guards, fill_guard_spot = \
        get_already_filled_guard_slot(watch_list, date, spot)

    guards = GuardsList(guards)

    if len(guards) == GUARD_SPOTS[spot]['guards_number']:
        return guards

    if fill_guard_spot:
        guard1, guard2 = get_next_available_guard(guards_list_prop,
                                                  watch_list,
                                                  date,
                                                  next_guards_to_place_when_available,
                                                  same_time_partners,
                                                  spot,
                                                  break_partners,
                                                  guards=guards)

        for g in [guard1, guard2]:
            if len(guards) != GUARD_SPOTS[spot]['guards_number'] and g:
                guards.append(g)

        if len(guards) == 1 and GUARD_SPOTS[spot]['guards_number'] == 2:
            guard2 = get_next_available_guard(guards_list_prop,
                                              watch_list,
                                              date,
                                              next_guards_to_place_when_available,
                                              same_time_partners,
                                              spot,
                                              break_partners,
                                              guards=guards,
                                              no_duo=True)[0]
            guards.append(guard2)
        guards.sort()

    return guards


def find_room(rooms, room):
    if isinstance(room, Room):
        room_number = room.number
    else:
        room_number = room

    for room in rooms:
        if room.number == room_number:
            return room
    return None


def find_last_duty_room_number(duty_rooms):
    if duty_rooms.keys():
        return duty_rooms[list(duty_rooms.keys())[-1]]


def find_kitat_konenout(watch_list, kitot_konenout_dict, rooms, date):
    if date in kitot_konenout_dict and kitot_konenout_dict[date]:
        return kitot_konenout_dict[date]

    kitot_konenout_rooms = list()
    for d in kitot_konenout_dict:
        kitat_konenout = kitot_konenout_dict[d]
        if kitat_konenout:
            found_room = find_room(rooms, kitat_konenout)
            if found_room and found_room.can_be_kitat_konenout \
                    and (not kitot_konenout_rooms or found_room != kitot_konenout_rooms[-1]):
                kitot_konenout_rooms.append(found_room)

    for room in rooms:
        if room not in kitot_konenout_rooms and room.can_be_kitat_konenout:
            kitot_konenout_rooms.insert(0, room)

    sorted_rooms = sorted(kitot_konenout_rooms, key=lambda r: r.get_available_guards_number(watch_list, date), reverse=True)

    i = 5
    while True:
        for room in sorted_rooms:
            available_soldiers = room.get_available_guards_number(watch_list, date)
            if room.number not in [r.number
                                   for r in kitot_konenout_rooms[len(kitot_konenout_rooms) - i:]] \
                    and available_soldiers >= MINIMUM_AVAILABLE_SOLDIERS_KITAT_CONENOUT:
                return room.number

        if i == 0:
            for room in sorted_rooms:
                if room.number not in [r.number
                                       for r in kitot_konenout_rooms[len(kitot_konenout_rooms) - 4:]]:
                    return room.number

        i -= 1


def is_date_needed(date, dates, first_hour_prop):
    midnight_date = get_day_at_midnight(date)
    if midnight_date == dates[0] and date.hour < first_hour_prop:
        return False

    # Remove unnecessary start and end of planning
    if (dates.index(midnight_date) == 0 and
            date.hour < FIRST_HOUR_FIRST_DATE) or \
            (dates.index(midnight_date) == len(dates) - 1 and
             date.hour >= LAST_HOUR_LAST_DATE):
        return False
    return True


def get_watch_list_data(guards_list_prop: GuardsList, watch_list, dates,
                        first_hour_prop, break_partners: bool):
    next_guards_to_place_when_available = GuardsList()
    same_time_partners = GuardsList()

    # Assign guards to each slot
    for date in dates:
        for hour in range(24):
            date = date.replace(hour=hour)

            if not is_date_needed(date, dates, first_hour_prop):
                continue

            spots = list(GUARD_SPOTS.keys())
            random.shuffle(spots)
            for spot in spots:
                guards = get_guards(guards_list_prop, watch_list, date,
                                    spot, next_guards_to_place_when_available,
                                    same_time_partners, break_partners)

                if len(guards) == GUARD_SPOTS[spot]['guards_number'] \
                        and not watch_list[date][spot]:
                    for g in guards:
                        g.last_spot = spot
                        if g in same_time_partners:
                            same_time_partners.remove(g)

                        if g in next_guards_to_place_when_available:
                            next_guards_to_place_when_available.remove(g)

                    watch_list[date][spot].extend(guards)

    sorted_watch_list = sort_watch_list(watch_list)

    return sorted_watch_list


def complete_duty_rooms(duty_rooms, dates, rooms, first_hour_prop):
    last_room = None
    need_new_room = True
    for date in dates:
        for hour in range(24):
            date = date.replace(hour=hour)

            if not is_date_needed(date, dates, first_hour_prop):
                continue

            if not TORANOUT_PROPS['start'] <= date.hour < TORANOUT_PROPS['end']:
                need_new_room = True
                duty_rooms[date] = ''
                continue

            if date in duty_rooms and duty_rooms[date]:
                last_room = duty_rooms[date]

            else:
                if not need_new_room and last_room:
                    room = last_room
                else:
                    need_new_room = False
                    rooms_cycle = cycle(rooms)
                    room = next(rooms_cycle)

                    if last_room:
                        while room != last_room:
                            room = next(rooms_cycle)

                        room = next(rooms_cycle)

                    first_room_in_loop = room
                    while not room.can_be_toran:
                        room = next(rooms_cycle)

                        # No room can be toran
                        if room == first_room_in_loop:
                            room = None
                            break

                last_room = room
                if room:
                    duty_rooms[date] = room
                else:
                    duty_rooms[date] = ''


def complete_kitot_konenout(watch_list, dates, first_hour_prop, rooms: [Room],
                            kitot_konenout_dict):
    kitat_konenout = None
    kitat_konenout_duration = 0
    for date in dates:
        for hour in range(24):
            date = date.replace(hour=hour)

            if not is_date_needed(date, dates, first_hour_prop):
                continue

            if kitot_konenout_dict[date]:
                kitat_konenout = None
                kitat_konenout_duration = 0
                continue

            # Complete kitot konenout
            if kitat_konenout_duration == KITAT_KONENOUT_DURATION:
                kitat_konenout = None
                kitat_konenout_duration = 0

            if not kitat_konenout:
                kitat_konenout = find_kitat_konenout(watch_list, kitot_konenout_dict, rooms, date)

            kitot_konenout_dict[date] = kitat_konenout
            kitat_konenout_duration += 1


def get_first_hour(watch_list, dates):
    # Get first hour of first date:
    first_hour = None
    for d in dates:
        for h in range(24):
            d = d.replace(hour=h)
            if d in watch_list.keys() and not first_hour:
                return h

    return 2


def get_dates(watch_list, days_num):
    dates = list()
    for d in watch_list:
        midnight_date = get_day_at_midnight(d)
        if midnight_date not in dates:
            dates.append(midnight_date)

    if not dates:
        dates = [get_day_at_midnight(datetime.now())]

    date = dates[-1]
    for i in range(days_num):
        date = date + timedelta(days=1)
        if date not in dates:
            dates.append(date)

    first_hour = get_first_hour(watch_list, dates)

    return dates, first_hour


def get_rooms(rooms_list, guards):
    rooms = list()
    for room_dict in rooms_list:
        room_guards = GuardsList([guards.find(guard)
                                  for guard in room_dict['guards']])
        room = Room(number=room_dict['number'], guards=room_guards,
                    can_be_toran=room_dict['can_be_toran'],
                    can_be_kitat_konenout=room_dict['can_be_kitat_konenout'])

        if room not in rooms:
            rooms.append(room)

    return rooms


def get_days_input():
    def is_integer(input_string):
        try:
            int(input_string)
            return True
        except ValueError:
            return False

    days_input = input("How many days do you need to schedule? ")

    while True:
        if is_integer(days_input):
            break
        else:
            days_input = input("Please enter a valid integer. ")
    print()

    return int(days_input)


def init(guards, print_unknown_names, days_input):
    if days_input is None:
        days_input = get_days_input()

    # Initialize the watch list
    watch_list = defaultdict(lambda: defaultdict(GuardsList))
    rooms = get_rooms(ROOMS_LIST, guards)
    watch_list, duty_rooms, kitot_konenout_dict = \
        get_previous_data(PREVIOUS_FILE_NAME, watch_list, guards, rooms,
                          print_unknown_names=print_unknown_names)
    missing_guards = get_missing_guards(MISSING_GUARDS_FILE_NAME,
                                        MISSING_GUARDS_SHEET_NAME,
                                        guards, days_input,
                                        print_unknown_guards=print_unknown_names)
    dates, first_hour = get_dates(watch_list, days_input)

    return watch_list, duty_rooms, kitot_konenout_dict, rooms, days_input, \
        dates, first_hour, missing_guards


def plan(user_input_prop, print_unknown_names, retry_after_infinite_loop_num=0,
         break_partners=False):
    user_i = user_input_prop
    try:
        if retry_after_infinite_loop_num >= RETRIES_NUM_BEFORE_CRASH:
            if break_partners:
                raise ImpossibleToFillPlanning
            else:
                return plan(user_i, print_unknown_names,
                            retry_after_infinite_loop_num=0,
                            break_partners=True)

        guards = deepcopy(GUARDS_LIST)
        watch_list, duty_rooms, kitot_konenout_dict, \
            rooms, user_i, dates, first_hour, _ = init(guards, print_unknown_names,
                                                       user_input_prop)
        complete_kitot_konenout(watch_list, dates, first_hour, rooms,
                                kitot_konenout_dict)
        complete_duty_rooms(duty_rooms, dates, rooms, first_hour)
        if user_i != -1:
            watch_list = get_watch_list_data(guards, watch_list, dates, first_hour,
                                             break_partners)
        delays_num = check_guards_slots_delays(watch_list, guards)

    except MaxIterationsReached:
        print("Oh oh, we got ourselves into a cul-de-sac, no guards available, retrying... Wish me luck!")
        return plan(user_i, False,
                    retry_after_infinite_loop_num=retry_after_infinite_loop_num + 1)

    return user_i, dates, delays_num, watch_list, duty_rooms, kitot_konenout_dict, guards, first_hour


if __name__ == '__main__':
    try_num = 0
    min_delays = 0
    best_wl = None
    user_input = None
    dates_list = list()
    guards_list = None
    duty_room_per_day = dict()
    kitot_konenout = dict()
    first_planning_hour = None
    try:
        while try_num < TRIES_NUMBER:
            user_input, dates_list, delays, wl, duty_room_per_day, \
                kitot_konenout, guards_list, first_planning_hour = plan(user_input, try_num == 0)

            if not min_delays or delays < min_delays:
                min_delays = delays
                best_wl = wl

            try_num += 1
            print(f'Try {try_num} finished')

            if user_input == -1:
                break

    except ImpossibleToFillPlanning:
        if not best_wl:
            raise ImpossibleToFillPlanning("Watch list can't be filled with this context, "
                                           "try to recruit more guards, remove some guard spots "
                                           "or reduce the MINIMAL_DELAY between each guard in consts file")

    check_guards_slots_delays(best_wl, guards_list, need_print=True)
    export_to_excel(NEW_WATCH_LIST_FILE_NAME, best_wl, GUARD_SPOTS,
                    duty_room_per_day, kitot_konenout)
    get_available_guards_per_date(best_wl, guards_list,
                                  NEW_WATCH_LIST_FILE_NAME,
                                  backward_delay=6, forward_delay=6)

    print('\nShivsakta!')
