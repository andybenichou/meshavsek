from datetime import datetime

from src.models.Guard import Guard
from src.models.GuardsList import GuardsList
from src.models.Spot import Spot, get_all_week_guard_spot


RANDOMNESS_LEVEL = 2  # Minimum 1. Use to avoid getting always the same result (guards always with the same people), the more the randomness, the worst the rest delays can be
MINIMAL_DELAY = 9  # Need to play with the start with the biggest delay then reduce it to get the best planning
PARTNER_MINIMAL_DELAY = 6  # Use to define what the minimal delay to consider a partner available for the guard with its partner
TRIES_NUMBER = 1  # Use more tries to get a better result
RETRIES_NUM_BEFORE_CRASH = 40

FIRST_HOUR_FIRST_DATE = 2  # To know when the planning start for the first day
LAST_HOUR_LAST_DATE = 20  # To knpw when to stop the planning on the last day

NEW_WATCH_LIST_FILE_NAME = 'watch_list'  # Output
PREVIOUS_FILE_NAME = 'שבצ״ק'  # Planning input file
MISSING_GUARDS_FILE_NAME = "פלוגה ג' - כל המידע מרוכז במקום אחד"  # Missing guard input file
MISSING_GUARDS_SHEET_NAME = 'כח אדם'
DAY_COLUMN_NAME = 'יום'
HOUR_COLUMN_NAME = 'שעה'
AVAILABLE_GUARDS_COLUMN_NAME = 'שומרים פנויים'
AVAILABLE_GUARDS_SHEET_NAME = 'Available'

# Spot names on the output files
GUARD_SPOTS = [
    Spot('SPOT_TEMPLATE_1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('SPOT_TEMPLATE_1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=0, duration=6)),
    Spot('SPOT_TEMPLATE_3', guard_duration=4, guards_number=2,
         guard_times={
             'א': {'start': 7, 'duration': 7},
             'ב': {'start': 7, 'duration': 7},
             'ג': {'start': 7, 'duration': 7},
             'ד': {'start': 7, 'duration': 7},
             'ה': {'start': 7, 'duration': 7},
         })
]

# Use to define the spots names on the input file
PREVIOUS_GUARD_SPOTS = [
    Spot('SPOT_TEMPLATE_1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('SPOT_TEMPLATE_2', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=0, duration=6)),
    Spot('SPOT_TEMPLATE_3', guard_duration=4, guards_number=2,
         guard_times={
             'א': {'start': 7, 'duration': 7},
             'ב': {'start': 7, 'duration': 7},
             'ג': {'start': 7, 'duration': 7},
             'ד': {'start': 7, 'duration': 7},
             'ה': {'start': 7, 'duration': 7},
             'ו': {'start': 7, 'duration': 7},
         }),
    Spot('SPOT_TEMPLATE_4', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
]

GUARDS_LIST = GuardsList(
    [Guard('Guard', '1',
           is_guarding=False,
           spots_preferences=['SPOT_TEMPLATE_1'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=23, hour=10),
               'end': datetime(year=2023, month=11, day=23, hour=23),
           },
           {
               'start': datetime(year=2023, month=11, day=24, hour=2),
               'end': datetime(year=2023, month=11, day=24, hour=23),
           }]),
     Guard('Guard', '2', partner='Guard 3'),
     Guard('Guard', '3', partner='Guard 2', is_living_far_away=True),
     Guard('Guard', '4', partner='Guard 5', is_living_far_away=True,
           same_time_partners=['Guard 6', 'Guard 7']),
     Guard('Guard', '5', partner='Guard 4', is_living_far_away=True,
           same_time_partners=['Guard 6', 'Guard 7']),
     Guard('Guard', '6', partner='Guard 7', is_living_far_away=True,
           same_time_partners=['Guard 4', 'Guard 5']),
     Guard('Guard', '7', partner='Guard 6',
           same_time_partners=['Guard 4', 'Guard 5']),
     Guard('Guard', '8', not_partners=['Guard 1']),
     Guard('Guard', '9',
           spots_preferences=list(filter(lambda spot: spot != 'ש.ג.',
                                         GUARD_SPOTS))),
     ])

# List of missing guards each date (in use only if no missing guards input file)
MISSING_GUARDS = {
    datetime(year=2023, month=11, day=24): ['Guard 1', 'Guard 2'],
    datetime(year=2023, month=11, day=25): ['Guard 5', 'Guard 3'],
}

ROOMS_LIST = [
    {
        'number': 1,
        'guards': ['Guard 1', 'Guard 2', 'Guard 3', 'Guard 4'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 2,
        'guards': ['Guard 6', 'Guard 7', 'Guard 8'],
        'can_be_toran': False,
        'can_be_kitat_konenout': True,
    },
]
