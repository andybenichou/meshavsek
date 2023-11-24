RANDOMNESS_LEVEL = 2  # Minimum 1. Use to avoid getting always the same result (guards always with the same people), the more the randomness, the worst the rest delays can be
MINIMAL_DELAY = 9  # Need to play with the start with the biggest delay then reduce it to get the best planning
PARTNER_MINIMAL_DELAY = 6  # Use to define what the minimal delay to consider a partner available for the guard with its partner
TRIES_NUMBER = 10  # Use more tries to get a better result
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