from Guard import Guard
from GuardsList import GuardsList

from consts import GUARD_SPOTS, WEEK_DAYS
from helper import get_next_week_day

GUARDS_LIST = GuardsList(
    [Guard('יואל', 'אודיז', partner='ארד רז',
           not_available_times=[{
               'start': {
                   'day': 'א',
                   'hour': 11,
               },
               'end': {
                   'day': 'ב',
                   'hour': 16,
               }
           }]),
     Guard('ארד', 'רז', partner='יואל אודיז',
           not_available_times=[{
               'start': {
                   'day': 'א',
                   'hour': 11,
               },
               'end': {
                   'day': 'ב',
                   'hour': 16,
               }
           }]),
     Guard('ליאור', 'אבו חמדה', is_living_far_away=True,
           spots_preferences=['ש.ג.', 'פטרול']),
     Guard("אבנר", "איזרבביץ'"),
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
     Guard('דובר', 'אלבז', partner='נריה כלפה', is_living_far_away=True,
           not_available_times=[{
               'start': {
                   'day': 'א',
                   'hour': 11,
               },
               'end': {
                   'day': 'ב',
                   'hour': 16,
               }
           }]),
     Guard('נריה', 'כלפה', partner='דובר אלבז',
           not_available_times=[{
               'start': {
                   'day': 'א',
                   'hour': 11,
               },
               'end': {
                   'day': 'ב',
                   'hour': 16,
               }
           }]),
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
     Guard('מיכאל', 'נפמן', partner='מאיר סדון'),
     Guard('מאיר', 'סדון', partner='מיכאל נפמן'),
     Guard('איתי', 'סיני', partner='לוטם עטיה'),
     Guard('לוטם', 'עטיה', partner='איתי סיני'),
     Guard('אור', 'נצקנסקי', spots_preferences=list(
         filter(lambda spot: spot != 'ש.ג.', GUARD_SPOTS.keys()))),
     Guard('מרדוש', 'דהאן', is_living_far_away=True),
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
               'start': {
                   'day': day,
                   'hour': 8,
               },
               'end': {
                   'day': get_next_week_day(day),
                   'hour': 5,
               }
           } for day in WEEK_DAYS])
     ])

# List of missing guards each day (not in use)
MISSING_GUARDS = {
    'א': ['מאיר סדון', 'מיכאל נפמן', 'סרגיי לומיאנסקי', 'שגיא אריה', 'עדן אסרף'],
    'ב': ['שמעון ספנייב', 'דימטרי יוספוב', 'סרגיי שבצוב', 'אור נצקנסקי', 'מיכאל ניסנוב', 'מיכאל נפמן', 'דורון לביא'],
    'ג': ['לואיס אברבוך', 'ארד רז', 'נדב קריספין', 'נריה כלפה', "אבנר איזרבביץ'", 'דעאל כהן', 'לוטם עטיה', 'מיכאל ניסנוב'],
    'ד': ['נתנאל שרעבי', 'דוד סספורטס', 'אנדי בנישו', 'אנזו גואטה', 'מיכאל ניסנוב', 'יואל אודיז',
          'ליאור אבו חמדה', 'איתי סיני', 'לוטם עטיה'],
    'ה': ['אסף זבולון', 'גיא פיאצה', 'יוסף רווה', 'אייל דבוש', 'משה אייכנשטין', 'שראל בלוך', 'מיכאל ניסנוב', 'לישי גרימו',
          'מרדש', 'אגומס מלדה', 'עמיחי נעים'],
    'ו': ['אלכסיי ברומברג', 'עומרי דותן', 'דובר אלבז', 'עמיחי נעים', 'ירין מטמוני', 'יהונתן דימנטמן', 'מיכאל ניסנוב',
          'יונתן יונג', 'שגיא אריה'],
    'שבת': ['אלכסיי ברומברג', 'עומרי דותן', 'דובר אלבז', 'עמיחי נעים', 'ירין מטמוני', 'יהונתן דימנטמן', 'מיכאל ניסנוב',
            'יונתן יונג', 'שגיא אריה']
}

ROOMS_LIST = [
    {
        'number': 5,
        'guards': ['מיכאל נפמן', 'מאיר סדון', 'איתי סיני', 'לואיס אברבוך', 'עמיחי נעים', 'עדן אסרף'],
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
        'guards': ['מאור ניקחה', 'נדב קריספין', 'אגומס מלדה', 'מיכאל ניסנוב', 'שגיא אריה', "אבנר איזרבביץ'"],
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
        'guards': ['מרדוש דהאן', 'איתי בהן', 'אייל דבוש', 'גיא פיאצה', 'נתנאל שרעבי', 'שראל בלוך'],
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
