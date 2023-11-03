from Guard import Guard
from GuardsList import GuardsList

from consts import GUARD_SPOTS, WEEK_DAYS
from helper import get_next_week_day

GUARDS_LIST = GuardsList(
    [Guard('יואל', partner='ארד'),
     Guard('ארד', partner='יואל'),
     Guard('ליאור', is_living_far_away=True),
     Guard('אבנר'),
     Guard('משה'),
     Guard('יונג'),
     Guard('דורון'),
     Guard('אסרף', partner='אסף'),
     Guard('אסף', partner='אסרף'),
     Guard('שגיא'),
     Guard('אנדי', partner='דוד', same_time_partners=['אנזו']),
     Guard('אנזו', same_time_partners=['דוד', 'אנדי']),
     Guard('דוד', partner='אנדי', same_time_partners=['אנזו']),
     Guard('דימנטמן', partner='מטמוני'),
     Guard('מטמוני', partner='דימנטמן'),
     Guard('דעאל', partner='אגומס'),
     Guard('אגומס', partner='דעאל'),
     Guard('ניסנוב'),
     Guard('לואיס'),
     Guard('דובר', partner='כלפה', is_living_far_away=True),
     Guard('כלפה', partner='דובר'),
     Guard('אלכסיי', partner='לומיאנסקי'),
     Guard('לומיאנסקי', partner='אלכסיי', is_living_far_away=True),
     Guard('איתי כהן', partner='עמיחי'),
     Guard('עמיחי', partner='איתי כהן'),
     Guard('שמעון'),
     Guard('דותן'),
     Guard('קריספין', partner='רווה', is_living_far_away=True),
     Guard('רווה', partner='קריספין'),
     Guard('דבוש', partner='פיאצה', is_living_far_away=True,
           same_time_partners=['שראל', 'שרעבי']),
     Guard('פיאצה', partner='דבוש', is_living_far_away=True,
           same_time_partners=['שראל', 'שרעבי']),
     Guard('שראל', partner='שרעבי', is_living_far_away=True,
           same_time_partners=['דבוש', 'פיאצה']),
     Guard('שרעבי', partner='שראל',
           same_time_partners=['דבוש', 'פיאצה']),
     Guard('דימה', partner='שבצוב'),
     Guard('שבצוב', partner='דימה'),
     Guard('נפמן', partner='סדון'),
     Guard('סדון', partner='נפמן'),
     Guard('סיני', partner='לוטם'),
     Guard('לוטם', partner='סיני'),
     Guard('אור', spots_preferences=list(
         filter(lambda spot: spot != 'ש.ג.', GUARD_SPOTS.keys()))),
     Guard('מרדש', is_living_far_away=True),
     Guard('בן', is_guarding=False),
     Guard('נח', is_guarding=False),
     Guard('לישי', is_guarding=False, is_living_far_away=True),
     Guard('מאור ניקחה', is_guarding=False),
     Guard('רועי', is_guarding=False),
     Guard('משה החופל', is_guarding=False,
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
    'א': ['סדון', 'נפמן', 'לומיאנסקי', 'שגיא', 'אסרף'],
    'ב': ['שמעון', 'דימה', 'שבצוב', 'אור', 'ניסנוב', 'נפמן', 'דורון'],
    'ג': ['לואיס', 'ארד', 'קריספין', 'כלפה', 'אבנר', 'דעאל', 'לוטם', 'ניסנוב'],
    'ד': ['שרעבי', 'דוד', 'אנדי', 'אנזו', 'ניסנוב', 'יואל',
          'ליאור', 'סיני', 'לוטם'],
    'ה': ['אסף', 'פיאצה', 'רווה', 'דבוש', 'משה', 'שראל', 'ניסנוב', 'לישי',
          'מרדש', 'אגומס', 'עמיחי'],
    'ו': ['אלכסיי', 'דותן', 'דובר', 'עמיחי', 'מטמוני', 'דימנטמן', 'ניסנוב',
          'יונג', 'שגיא'],
    'שבת': ['אלכסיי', 'דותן', 'דובר', 'עמיחי', 'מטמוני', 'דימנטמן', 'ניסנוב',
            'יונג', 'שגיא']
}

ROOMS_LIST = [
    {
        'number': 5,
        'guards': ['נפמן', 'סדון', 'סיני', 'לואיס', 'עמיחי', 'אסרף'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 6,
        'guards': ['משה', 'דעאל', 'דוד', 'אנדי', 'אנזו'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 7,
        'guards': ['מאור ניקחה', 'קריספין', 'אגומס', 'ניסנוב', 'שגיא', 'אבנר'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 8,
        'guards': ['אסף', 'שבצוב', 'דימה', 'דימנטמן', 'מטמוני'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 9,
        'guards': ['רווה', 'אור', 'יונג', 'לוטם', 'לישי'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 10,
        'guards': ['מרדש', 'איתי בהן', 'דבוש', 'פיאצה', 'שרעבי', 'שראל'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 11,
        'guards': ['יואל', 'כלפה', 'ארד', 'דובר', 'לומיאנסקי', 'שמעון'],
        'can_be_toran': True,
        'can_be_kitat_konenout': True,
    },
    {
        'number': 12,
        'guards': ['דותן', 'ליאור', 'נח', 'בן', 'רועי'],
        'can_be_toran': False,
        'can_be_kitat_konenout': False,
    },
]
