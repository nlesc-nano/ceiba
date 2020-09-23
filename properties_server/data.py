"""Module to test the interface."""

PROPERTIES = [{
    "id": 0, "smile": "O=O",
    "collection_name": "pbedzp",
    "geometry": "2\n\nO 0.0 0.0 0.0\nO 0.0 0.0 1.208",
    "data": '{"scscore": 1.5, "bulkiness": 2.0}'
},
    {
    "id": 343, "smile": "CC(=O)O",
    "collection_name": "pbedzp",
    "geometry": None,
    "data": None
},
    {
    "id": 10245, "smile": "CCCCCCCCC=CCCCCCCCC(=O)O",
    "collection_name": "pbedzp",
    "geometry": None,
    "data": None
}
]

JOBS = [
    {"id": 33444, "property": PROPERTIES[0],
     "settings": "{}",
     "status": "DONE",
     "user": "felipez",
     "schedule_time": 1600776842.278506,
     "completion_time": 1600781352.866547,
     "platform": 'Linux-5.4.0-47-generic-x86_64-with-glibc2.10'
     },
    {"id": 1034, "property": PROPERTIES[1],
     "settings": "{}",
     "status": "AVAILABLE",
     "user": None, "schedule_time": None,
     "completion_time": None, "platform": None},
    {"id": 135037, "property": PROPERTIES[2],
     "settings": "{}",
     "status": "AVAILABLE",
     "user": None, "schedule_time": None,
     "completion_time": None, "platform": None}
]