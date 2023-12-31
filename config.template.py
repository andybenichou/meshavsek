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
# Cinfug template file of the project Meshavshek


RANDOMNESS_LEVEL = 2  # Minimum 1. Use to avoid getting always the same result (guards always with the same people), the more the randomness, the worst the rest delays can be
MINIMAL_DELAY = 9  # Need to play with the start with the biggest delay then reduce it to get the best planning
PARTNER_MINIMAL_DELAY = 6  # Use to define what the minimal delay to consider a partner available for the guard with its partner
TRIES_NUMBER = 10  # Use more tries to get a better result
RETRIES_NUM_BEFORE_CRASH = 40

FIRST_HOUR_FIRST_DATE = 2  # To know when the planning start for the first day
LAST_HOUR_LAST_DATE = 20  # To know when to stop the planning on the last day

# Define home hours by distance from the base to home and
# according to the day back
HOME_HOURS = {
    'exit': {
        'regular': 12,
        'far_away': 10,
    },
    'return': {
        'regular': {
            'week_day': 12,
            'shabbat': 21,
        },
        'far_away': {
            'week_day': 16,
            'shabbat': 23,
        }
    }
}

# Define hapak hours
HAPAK_HOURS = {
    'start': {
        'hour': 12,
    },
    'end': {
        'same_day': False,
        'hour': 12,
    }
}

NEW_WATCH_LIST_FILE_NAME = 'watch_list'  # Output
PREVIOUS_FILE_NAME = 'Previous_planning'  # Planning input file
MISSING_GUARDS_FILE_NAME = "Guards"  # Missing guard input file
MISSING_GUARDS_SHEET_NAME = 'כח אדם'
DAY_COLUMN_NAME = 'יום'
HOUR_COLUMN_NAME = 'שעה'
AVAILABLE_GUARDS_COLUMN_NAME = 'שומרים פנויים'
AVAILABLE_GUARDS_SHEET_NAME = 'Available'
