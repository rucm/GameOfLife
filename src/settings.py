import json


general = json.dumps([
    {
        'type': 'title',
        'title': 'General'
    },
    {
        'type': 'numeric',
        'title': 'Speed',
        'section': 'gameoflife',
        'desc': 'Number of updates per second',
        'key': 'speed'
    }
])

