RANDOMNESS_LEVEL = 2
MINIMAL_DELAY = 18
PARTNER_MINIMAL_DELAY = 9
TRIES_NUMBER = 20
RETRIES_NUM_BEFORE_CRASH = 20

NEW_WATCH_LIST_FILE_NAME = 'watch_list'
PREVIOUS_FILE_NAME = 'שבצ״ק'
MISSING_GUARDS_FILE_NAME = "פלוגה ג' - כל המידע מרוכז במקום אחד"
MISSING_GUARDS_SHEET_NAME = 'כח אדם'

WEEK_DAYS = ['א', 'ב', 'ג', 'ד', 'ה', 'ו', 'שבת']
ENGLISH_WEEKDAY_TO_HEBREW = {
    'Sunday': 'א',
    'Monday': 'ב',
    'Tuesday': 'ג',
    'Wednesday': 'ד',
    'Thursday': 'ה',
    'Friday': 'ו',
    'Saturday': 'שבת',
}

FIRST_HOUR_FIRST_DATE = 2
LAST_HOUR_LAST_DATE = 23

KITAT_KONENOUT_DURATION = 6
MINIMUM_AVAILABLE_SOLDIERS_KITAT_CONENOUT = 2

GUARD_SPOTS = {
    'ש.ג.': {
        'start': 2,
        'duration': 24,
        'guard_duration': 3,
        'guards_number': 2,
    },
    'בטונדות': {
        'start': 2,
        'duration': 24,
        'guard_duration': 3,
        'guards_number': 2,
    },
    'סיור': {
        'start': 22,
        'duration': 8,
        'guard_duration': 4,
        'guards_number': 2,
    }
}

PREVIOUS_GUARD_SPOTS = {
    'ש.ג.': {
        'start': 2,
        'duration': 24,
        'guard_duration': 3,
        'guards_number': 2,
    },
    'בטונדות': {
        'start': 2,
        'duration': 24,
        'guard_duration': 3,
        'guards_number': 2,
    },
    'סיור': {
        'start': 22,
        'duration': 8,
        'guard_duration': 4,
        'guards_number': 2,
    }
}

TORANOUT_PROPS = {
    'column_name': 'תורנות',
    'start': 10,
    'end': 20,
}

KITOT_KONENOUT_PROPS = {
    'column_name': 'כתת כוננות',
    'start': None,
    'end': None,
    'duration': 6,
}

DAY_COLUMN_NAME = 'יום'
HOUR_COLUMN_NAME = 'שעה'
AVAILABLE_GUARDS_COLUMN_NAME = 'שומרים פנויים'

AVAILABLE_GUARDS_SHEET_NAME = 'Available'
