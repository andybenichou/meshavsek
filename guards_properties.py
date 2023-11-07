from datetime import datetime, timedelta

from Guard import Guard
from GuardsList import GuardsList

from consts import GUARD_SPOTS
from helper import get_day_at_midnight

GUARDS_LIST = GuardsList(
    [Guard('יואל', 'אודיז', partner='ארד רז'),
     Guard('ארד', 'רז', partner='יואל אודיז'),
     Guard('ליאור', 'אבו חמדה', is_living_far_away=True,
           spots_preferences=['ש.ג.', 'פטרול']),
     Guard("אבנר", "איזרבביץ"),
     Guard('משה', 'אייכנשטין'),
     Guard('יונתן', 'יונג'),
     Guard('דורון', 'לביא'),
     Guard('עדן', 'אסרף', partner='אסף זבולון'),
     Guard('אסף', 'זבולון', partner='עדן אסרף'),
     Guard('שגיא', 'אריה'),
     Guard('אנדי', 'בנישו', partner='דוד סספורטס', same_time_partners=['אנזו גואטה']),
     Guard('אנזו', 'גואטה', same_time_partners=['דוד סספורטס', 'אנדי בנישו']),
     Guard('דוד', 'סספורטס', partner='אנדי בנישו', same_time_partners=['אנזו גואטה']),
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
     Guard('יוסף', 'רווה', partner='נדב קריספין'),
     Guard('אייל', 'דבוש', partner='גיא פיאצה', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי']),
     Guard('גיא', 'פיאצה', partner='אייל דבוש', is_living_far_away=True,
           same_time_partners=['שראל בלוך', 'נתנאל שרעבי']),
     Guard('שראל', 'בלוך', partner='נתנאל שרעבי', is_living_far_away=True,
           same_time_partners=['אייל דבוש', 'גיא פיאצה']),
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
     Guard('משה', 'החופל', is_guarding=False,
           spots_preferences=['פנטאוז'],
           time_preferences=[{
               'start': 5,
               'end': 8,
           }],
           not_available_times=[{
               'start': (get_day_at_midnight(datetime.now()) + timedelta(days=i + 1)).replace(hour=8),
               'end': (get_day_at_midnight(datetime.now()) + timedelta(days=i + 1)).replace(hour=5),
           } for i in range(180)])
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
        'guards': ['מאור ניקחה', 'נדב קריספין', 'אגומס מלדה', 'מיכאל ניסנוב', 'שגיא אריה', "אבנר איזרבביץ"],
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
