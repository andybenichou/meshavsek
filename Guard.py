from itertools import cycle

# Define the week days
week_days = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'שבת']


class Guard:
    def __init__(self, name, guards_slots=None, not_available_times=None):
        self.name = name
        self.__guards_slots = guards_slots if guards_slots else list()
        self.__not_available_times = not_available_times \
            if not_available_times else list()

    def __repr__(self):
        return f"Guard(name={self.name!r})"

    def __str__(self):
        return self.name

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
