import json


game = json.dumps([
    {
        'type': 'title',
        'title': 'Game of Life'
    },
    {
        'type': 'numeric',
        'title': 'Speed',
        'section': 'game',
        'desc': 'Number of updates per second',
        'key': 'speed'
    }
])