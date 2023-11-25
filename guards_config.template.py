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
# Guards config template file of the project Meshavshek

from datetime import datetime

from src.models.Guard import Guard
from src.models.GuardsList import GuardsList
from src.models.Spot import Spot, get_all_week_guard_spot

# Spot names on the output files
GUARD_SPOTS = [
    Spot('עמדה 1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('עמדה 2', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('עמדה 3', guard_duration=4, guards_number=2,
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
    Spot('עמדה 1', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('עמדה 2', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('עמדה 3', guard_duration=3, guards_number=2,
         guard_times={
             'א': {'start': 8, 'duration': 9},
             'ב': {'start': 8, 'duration': 9},
             'ג': {'start': 8, 'duration': 9},
             'ד': {'start': 8, 'duration': 9},
             'ה': {'start': 8, 'duration': 9},
         }),
    Spot('עמדה 3', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=10, duration=6)),
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
    [Guard('שומר', '1',
           spots_preferences=['עמדה 1'],
           not_available_times=[{
                   'start': datetime(year=2023, month=11, day=24, hour=10),
                   'end': datetime(year=2023, month=11, day=24, hour=23),
                },
               {
                   'start': datetime(year=2023, month=11, day=25, hour=2),
                   'end': datetime(year=2023, month=11, day=25, hour=23),
               }]),
     Guard('שומר', '2', partner='שומר 3'),
     Guard('שומר', '3', partner='שומר 2', is_living_far_away=True),
     Guard('שומר', '4'),
     Guard('שומר', '5', partner='שומר 6', is_living_far_away=True,
           same_time_partners=['שומר 7', 'שומר 8']),
     Guard('שומר', '6', partner='שומר 5', is_living_far_away=True,
           same_time_partners=['שומר 7', 'שומר 8']),
     Guard('שומר', '7', partner='שומר 8', is_living_far_away=True,
           same_time_partners=['שומר 5', 'שומר 6']),
     Guard('שומר', '8', partner='שומר 7',
           same_time_partners=['שומר 5', 'שומר 6']),
     Guard('שומר', '9',
           spots_preferences=list(filter(lambda spot: spot != 'עמדה 1',
                                         GUARD_SPOTS))),
     Guard('שומר', '10', is_guarding=False),
     ])

# List of missing guards each date (in use only if no missing guards input file)
MISSING_GUARDS = {
    datetime(year=2023, month=11, day=23): ['שומר 1', 'שומר 2', 'שומר 3'],
    datetime(year=2023, month=11, day=24): ['שומר 5', 'שומר 8', 'שומר 10'],
}

ROOMS_LIST = [
    {
        'number': 1,
        'guards': ['שומר 1', 'שומר 2', 'שומר 3'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 2,
        'guards': ['שומר 5', 'שומר 8', 'שומר 10'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 3,
        'guards': ['שומר 4', 'שומר 6', 'שומר 7', 'שומר 9'],
        'can_be_toran': False,
        'can_be_kitat_konenout': False,
    },
]
