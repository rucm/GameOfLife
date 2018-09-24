import json


game = json.dumps([
    {
        'type': 'title',
        'title': 'General'
    },
    {
        'type': 'numeric',
        'title': 'Speed',
        'section': 'cell_grid',
        'desc': 'Number of updates per second',
        'key': 'speed'
    }
])
