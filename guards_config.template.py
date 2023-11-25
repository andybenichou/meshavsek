from datetime import datetime

from src.models.Guard import Guard
from src.models.GuardsList import GuardsList
from src.models.Spot import Spot, get_all_week_guard_spot

# Spot names on the output files
GUARD_SPOTS = [
    Spot('Spot 1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('Spot 2', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('Spot 3', guard_duration=4, guards_number=2,
         guard_times={
             'א': {'start': 7, 'duration': 7},
             'ב': {'start': 10, 'duration': 7},
             'ג': {'start': 7, 'duration': 7},
             'ד': {'start': 7, 'duration': 7},
             'ה': {'start': 4, 'duration': 7},
         })
]

# Use to define the spots names on the input file
PREVIOUS_GUARD_SPOTS = [
    Spot('Spot 1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('Spot 2', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('Spot 3', guard_duration=4, guards_number=2,
         guard_times={
             'א': {'start': 7, 'duration': 10},
             'ב': {'start': 7, 'duration': 10},
             'ג': {'start': 7, 'duration': 10},
             'ד': {'start': 7, 'duration': 10},
             'ה': {'start': 7, 'duration': 10},
         }),
    Spot('Spot 3', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=0, duration=6)),
]

TORANOUT_PROPS = {
    'is_needed': False,
    'column_name': 'תורנות',
    'start': 10,
    'end': 20,
}

KITOT_KONENOUT_PROPS = {
    'is_needed': False,
    'column_name': 'כתת כוננות',
    'start': None,
    'end': None,
    'duration': 6,
    'minimum_available_soldiers': 2,
}

GUARDS_LIST = GuardsList(
    [Guard('Guard', '1',
           spots_preferences=['Spot 1'],
           not_available_times=[{
                   'start': datetime(year=2023, month=11, day=24, hour=10),
                   'end': datetime(year=2023, month=11, day=24, hour=23),
                },
               {
                   'start': datetime(year=2023, month=11, day=25, hour=2),
                   'end': datetime(year=2023, month=11, day=25, hour=23),
               }]),
     Guard('Guard', '2', partner='Guard 3'),
     Guard('Guard', '3', partner='Guard 2', is_living_far_away=True),
     Guard('Guard', '4'),
     Guard('Guard', '5', partner='Guard 6', is_living_far_away=True,
           same_time_partners=['Guard 7', 'Guard 8']),
     Guard('Guard', '6', partner='Guard 5', is_living_far_away=True,
           same_time_partners=['Guard 7', 'Guard 8']),
     Guard('Guard', '7', partner='Guard 8', is_living_far_away=True,
           same_time_partners=['Guard 5', 'Guard 6']),
     Guard('Guard', '8', partner='Guard 7',
           same_time_partners=['Guard 5', 'Guard 6']),
     Guard('Guard', '9',
           spots_preferences=list(filter(lambda spot: spot != 'Spot 1',
                                         GUARD_SPOTS))),
     Guard('Guard', '10', is_guarding=False),
     ])

# List of missing guards each date (in use only if no missing guards input file)
MISSING_GUARDS = {
    datetime(year=2023, month=11, day=23): ['Guard 1', 'Guard 2', 'Guard 3'],
    datetime(year=2023, month=11, day=24): ['Guard 5', 'Guard 8', 'Guard 10'],
}

ROOMS_LIST = [
    {
        'number': 1,
        'guards': ['Guard 1', 'Guard 2', 'Guard 3'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 2,
        'guards': ['Guard 5', 'Guard 8', 'Guard 10'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 3,
        'guards': ['Guard 4', 'Guard 6', 'Guard 7', 'Guard 9'],
        'can_be_toran': False,
        'can_be_kitat_konenout': False,
    },
]
