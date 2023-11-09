from datetime import datetime

from Guard import Guard
from GuardsList import GuardsList

from consts import GUARD_SPOTS

GUARDS_LIST = GuardsList(
    [Guard('משה', 'החופל', is_guarding=True,
           spots_preferences=['בטונדות'],
           time_preferences=[{
               'start': 5,
               'end': 8,
           }],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=12, hour=5),
               'end': datetime(year=2023, month=11, day=12, hour=8),
           }]),
     Guard('יואל', 'אודיז', partner='ארד רז'),
     Guard('ארד', 'רז', partner='יואל אודיז'),
     Guard('ליאור', 'אבו חמדה', is_living_far_away=True,
           spots_preferences=['ש.ג.']),
     Guard("אבנר", "יוזפוביץ",
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=13, hour=15),
               'end': datetime(year=2023, month=11, day=14, hour=11),
           }]),
     Guard('משה', 'אייכנשטין'),
     Guard('יונתן', 'יונג', is_living_far_away=True),
     Guard('דורון', 'לביא'),
     Guard('עדן', 'אסרף', partner='אסף זבולון'),
     Guard('אסף', 'זבולון', partner='עדן אסרף'),
     Guard('שגיא', 'אריה'),
     Guard('אנדי', 'בנישו', partner='דוד סספורטס',
           same_time_partners=['אנזו גואטה'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=10, hour=8),
               'end': datetime(year=2023, month=11, day=10, hour=12),
           }]),
     Guard('אנזו', 'גואטה',
           same_time_partners=['דוד סספורטס', 'אנדי בנישו'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=10, hour=8),
               'end': datetime(year=2023, month=11, day=10, hour=12),
           }]),
     Guard('דוד', 'סספורטס', partner='אנדי בנישו',
           same_time_partners=['אנזו גואטה'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=10, hour=8),
               'end': datetime(year=2023, month=11, day=10, hour=12),
           }]),
     Guard('יהונתן', 'דימנטמן', partner='ירין מטמוני'),
     Guard('ירין', 'מטמוני', partner='יהונתן דימנטמן'),
     Guard('דעאל', 'כהן', partner='אגומס מלדה'),
     Guard('אגומס', 'מלדה', partner='דעאל כהן'),
     Guard('מיכאל', 'ניסנוב'),
     Guard('לואיס', 'אברבוך'),
     Guard('דובר', 'אלבז', partner='נריה כלפה', is_living_far_away=True),
     Guard('נריה', 'כלפה', partner='דובר אלבז'),
     Guard('אלכסיי', 'ברומברג', partner='סרגיי לומיאנסקי'),
     Guard('סרגיי', 'לומיאנסקי', partner='אלכסיי ברומברג', is_living_far_away=True),
     Guard('איתי', 'כהן', partner='עמיחי נעים'),
     Guard('עמיחי', 'נעים', partner='איתי כהן'),
     Guard('שמעון', 'ספנייב'),
     Guard('עומרי', 'דותן'),
     Guard('נדב', 'קריספין', partner='יוסף רווה', is_living_far_away=True),
     Guard('יוסף', 'רווה', partner='נדב קריספין',
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=8, hour=12),
               'end': datetime(year=2023, month=11, day=9, hour=10),
           }]),
     Guard('אייל', 'דבוש', partner='גיא פיאצה', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=8, hour=12),
               'end': datetime(year=2023, month=11, day=9, hour=14),
           }]),
     Guard('גיא', 'פיאצה', partner='אייל דבוש', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=8, hour=12),
               'end': datetime(year=2023, month=11, day=9, hour=14),
           }]),
     Guard('שראל', 'בלוך', partner='נתנאל שרעבי', is_living_far_away=True,
           same_time_partners=['אייל דבוש', 'גיא פיאצה'],
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=8, hour=12),
               'end': datetime(year=2023, month=11, day=9, hour=14),
           }]),
     Guard('אדיר', '', is_guarding=False,
           not_available_times=[{
               'start': datetime(year=2023, month=11, day=8, hour=12),
               'end': datetime(year=2023, month=11, day=9, hour=14),
           }]),
     Guard('נתנאל', 'שרעבי', partner='שראל בלוך',
           same_time_partners=['אייל דבוש', 'גיא פיאצה']),
     Guard('דימטרי', 'יוספוב', partner='סרגיי שבצוב'),
     Guard('סרגיי', 'שבצוב', partner='דימטרי יוספוב'),
     Guard('מיכאל', 'נפמן', partner='מאור סדון'),
     Guard('מאור', 'סדון', partner='מיכאל נפמן'),
     Guard('איתי', 'סיני', partner='לוטם עטיה'),
     Guard('לוטם', 'עטיה', partner='איתי סיני'),
     Guard('אור', 'נצקנסקי',
           spots_preferences=list(filter(lambda spot: spot != 'ש.ג.',
                                         GUARD_SPOTS.keys()))),
     Guard('מרדוש', 'דהן', is_living_far_away=True),
     Guard('בן', 'עידה', is_guarding=False),
     Guard('נח', 'טואטי', is_guarding=False),
     Guard('לישי', 'גרימו', is_guarding=False, is_living_far_away=True),
     Guard('מאור', 'ניקחה', is_guarding=False),
     Guard('רועי', 'קלפסקי', is_guarding=False),
     Guard('בן', 'בנימין'),
     Guard('איתמר', 'בנימין'),
     Guard('גיל', 'אורון', is_guarding=False),
     Guard('אלדד', 'הלל', is_guarding=False),
     ])

# List of missing guards each date (not in use)
MISSING_GUARDS = {}

ROOMS_LIST = [
    {
        'number': 5,
        'guards': ['מיכאל נפמן', 'מאור סדון', 'איתי סיני', 'לואיס אברבוך', 'עמיחי נעים', 'עדן אסרף'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 6,
        'guards': ['משה אייכנשטין', 'דעאל כהן', 'דוד סספורטס', 'אנדי בנישו', 'אנזו גואטה'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 7,
        'guards': ['מאור ניקחה', 'נדב קריספין', 'אגומס מלדה', 'מיכאל ניסנוב', 'שגיא אריה', "אבנר יוזפוביץ"],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 8,
        'guards': ['אסף זבולון', 'סרגיי שבצוב', 'דימטרי יוספוב', 'יהונתן דימנטמן', 'ירין מטמוני'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 9,
        'guards': ['יוסף רווה', 'אור נצקנסקי', 'יונתן יונג', 'לוטם עטיה', 'לישי גרימו'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 10,
        'guards': ['מרדוש דהן', 'איתי בהן', 'אייל דבוש', 'גיא פיאצה', 'נתנאל שרעבי', 'שראל בלוך'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 11,
        'guards': ['יואל אודיז', 'נריה כלפה', 'ארד רז', 'דובר אלבז', 'סרגיי לומיאנסקי', 'שמעון ספנייב'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 12,
        'guards': ['עומרי דותן', 'ליאור אבו חמדה', 'נח טואטי', 'בן עידה', 'רועי קלפסקי'],
        'can_be_toran': False,
        'can_be_kitat_konenout': False,
    },
]
