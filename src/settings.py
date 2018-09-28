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
    },
    {
        'type': 'numeric',
        'title': 'Cols',
        'section': 'gameoflife',
        'desc': 'Number of cols of cells',
        'key': 'cols'
    },
    {
        'type': 'numeric',
        'title': 'Rows',
        'section': 'gameoflife',
        'desc': 'Number of rows of cells',
        'key': 'rows'
    }
])
