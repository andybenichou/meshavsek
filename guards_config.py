from datetime import datetime

from src.models.Guard import Guard
from src.models.GuardsList import GuardsList
from src.models.Spot import Spot, get_all_week_guard_spot

# Spot names on the output files
GUARD_SPOTS = [
    Spot('ש.ג.', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('בטונדות', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('סיור', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=0, duration=6)),
    Spot('מרחבים', guard_duration=4, guards_number=2,
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
    Spot('ש.ג.', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('בטונדות', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=2)),
    Spot('סיור', guard_duration=3, guards_number=2,
         guard_times=get_all_week_guard_spot(start=0, duration=6)),
    Spot('מרחבים', guard_duration=4, guards_number=2,
         guard_times={
             'א': {'start': 7, 'duration': 7},
             'ב': {'start': 7, 'duration': 7},
             'ג': {'start': 7, 'duration': 7},
             'ד': {'start': 7, 'duration': 7},
             'ה': {'start': 7, 'duration': 7},
             'ו': {'start': 7, 'duration': 7},
         })
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
    [Guard('משה', 'החופל', is_guarding=False,
           spots_preferences=['בטונדות'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=23, hour=10),
               'end': datetime(year=2023, month=11, day=23, hour=23),
           },
           {
               'start': datetime(year=2023, month=11, day=24, hour=2),
               'end': datetime(year=2023, month=11, day=24, hour=23),
           }]),
     Guard('יואל', 'אודיז', partner='ארד רז'),
     Guard('ארד', 'רז', partner='יואל אודיז', is_living_far_away=True),
     Guard('ליאור', 'אבו חמדה', is_living_far_away=True,
           spots_preferences=['ש.ג.'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=17, hour=20),
               'end': datetime(year=2023, month=11, day=18, hour=23),
           }]),
     Guard("אבנר", "יוזפוביץ"),
     Guard('יונתן', 'יונג', is_living_far_away=True),
     Guard('דורון', 'לביא'),
     Guard('עדן', 'אסרף', partner='איתי סיני'),
     Guard('אסף', 'זבולון'),
     Guard('שגיא', 'אריה'),
     Guard('אנדי', 'בנישו', partner='דוד סספורטס'),
     Guard('דוד', 'סספורטס', partner='אנדי בנישו'),
     Guard('יהונתן', 'דימנטמן', partner='ירין מטמוני'),
     Guard('ירין', 'מטמוני', partner='יהונתן דימנטמן'),
     Guard('דעאל', 'כהן', partner='אגומס מלדה'),
     Guard('אגומס', 'מלדה', partner='דעאל כהן'),
     Guard('מיכאל', 'ניסנוב'),
     Guard('לואיס', 'אברבוך'),
     Guard('דובר', 'אלבז', partner='נריה כלפה', is_living_far_away=True),
     Guard('נריה', 'כלפה', partner='דובר אלבז'),
     Guard('אלכסיי', 'ברומברג'),
     Guard('איתי', 'כהן', partner='עמיחי נעים',
           spots_preferences=['בטונדות', 'ש.ג.']),
     Guard('עמיחי', 'נעים', partner='איתי כהן'),
     Guard('עומרי', 'דותן',
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=17, hour=20),
               'end': datetime(year=2023, month=11, day=18, hour=17),
           }]),
     Guard('נדב', 'קריספין', partner='יוסף רווה', is_living_far_away=True),
     Guard('יוסף', 'רווה', partner='נדב קריספין'),
     Guard('אייל', 'דבוש', partner='גיא פיאצה', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי']),
     Guard('גיא', 'פיאצה', partner='אייל דבוש', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי']),
     Guard('שראל', 'בלוך', partner='נתנאל שרעבי', is_living_far_away=True,
           same_time_partners=['אייל דבוש', 'גיא פיאצה']),
     Guard('אדיר', 'מור',
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=16, hour=17),
               'end': datetime(year=2023, month=11, day=17, hour=5),
           }]),
     Guard('נתנאל', 'שרעבי', partner='שראל בלוך',
           same_time_partners=['אייל דבוש', 'גיא פיאצה']),
     Guard('דימטרי', 'יוספוב', partner='סרגיי שבצוב',
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=16, hour=17),
               'end': datetime(year=2023, month=11, day=17, hour=8),
           }]),
     Guard('סרגיי', 'שבצוב', partner='דימטרי יוספוב',
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=16, hour=17),
               'end': datetime(year=2023, month=11, day=17, hour=8),
           }]),
     Guard('איתי', 'סיני', partner='עדן אסרף'),
     Guard('לוטם', 'עטיה', not_partners=['אסף זבולון']),
     Guard('אור', 'נצקנסקי',
           spots_preferences=list(filter(lambda spot: spot != 'ש.ג.',
                                         GUARD_SPOTS))),
     Guard('מרדוש', 'דהן', is_living_far_away=True),
     Guard('בן', 'עידה', is_guarding=False),
     Guard('נח', 'טואטי', is_guarding=False),
     Guard('לישי', 'גרימו', is_guarding=False, is_living_far_away=True),
     Guard('מאור', 'ניקחה', is_guarding=False),
     Guard('רועי', 'קלפסקי', is_guarding=False),
     Guard('בן', 'בנימין'),
     Guard('איתמר', 'בנימין', is_living_far_away=True,
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=24, hour=6),
               'end': datetime(year=2023, month=11, day=24, hour=23),
           }]),
     Guard('גיל', 'אורון', is_guarding=False),
     Guard('פביאן', 'חויוס'),
     Guard('חן', 'טלה'),
     Guard('יניב', 'משה'),
     Guard('זיטר', 'יצחק'),
     Guard('ראובן', 'מאור'),
     Guard('אלקנה', 'שפנגנטל'),
     ])

# List of missing guards each date (in use only if no missing guards input file)
MISSING_GUARDS = {}

ROOMS_LIST = [
    {
        'number': 5,
        'guards': ['איתי סיני', 'לואיס אברבוך', 'עמיחי נעים', 'עדן אסרף'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 6,
        'guards': ['דעאל כהן', 'דוד סספורטס', 'אנדי בנישו'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 7,
        'guards': ['מאור ניקחה', 'נדב קריספין', 'אגומס מלדה', 'מיכאל ניסנוב',
                   'שגיא אריה', "אבנר יוזפוביץ"],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 8,
        'guards': ['אסף זבולון', 'סרגיי שבצוב', 'דימטרי יוספוב',
                   'יהונתן דימנטמן', 'ירין מטמוני'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 9,
        'guards': ['יוסף רווה', 'אור נצקנסקי', 'יונתן יונג', 'לוטם עטיה',
                   'לישי גרימו'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 10,
        'guards': ['מרדוש דהן', 'איתי כהן', 'אייל דבוש', 'גיא פיאצה',
                   'נתנאל שרעבי', 'שראל בלוך'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 11,
        'guards': ['יואל אודיז', 'נריה כלפה', 'ארד רז', 'דובר אלבז'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 12,
        'guards': ['עומרי דותן', 'ליאור אבו חמדה', 'נח טואטי', 'בן עידה',
                   'רועי קלפסקי'],
        'can_be_toran': False,
        'can_be_kitat_konenout': False,
    },
]
