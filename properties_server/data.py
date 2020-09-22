"""Module to test the interface."""

PROPERTIES = [{
    "id": 0, "smile": "O=O",
    "theory_level": "pbe/dzp",
    "geometry": "2\n\nO 0.0 0.0 0.0\nO 0.0 0.0 1.208",
    "values": {"scscore": 1.5, "bulkiness": 2.0}
},
    {
    "id": 0, "smile": "CC(=O)O",
    "theory_level": "pbe/dzp",
    "geometry": None,
    "values": None
}
]

JOBS = [
    {"id": 1034, "property": PROPERTIES[1],
     "settings": "{}",
     "status": "AVAILABLE",
     "user": None, "schedule_time": None, "completion_time": None, "platform": None},
    {"id": 33444, "property": PROPERTIES[0],
     "settings": "{}",
     "status": "DONE",
     "user": "felipez",
     "schedule_time": 1600776842.278506,
     "completion_time": 1600781352.866547,
     "platform": 'Linux-5.4.0-47-generic-x86_64-with-glibc2.10'
     }
]