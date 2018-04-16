import json
from datetime import timedelta
import dateutil.parser as parser


class Schedule():
    def __init__(self, filename):
        self.filename = filename
        self.events = []
        self.locations = []
        self.load()

    def load(self):
        raw = json.load(open(self.filename))
        self.events = {event['id']: Event(event['name'],
                                          start=event['start'],
                                          duration=event['duration'],
                                          location_id=event['location_id'])
                       for event in raw['events']}

        self.locations = {location['id']: Location(location['name'])
                          for location in raw['locations']}

    def with_location_name(self, name):
        return [event for key, event in self.events.items()
                if self.locations[event.location_id].name == name]

    def events_at(self, time):
        return [event for id, event in self.events.items()
                if event.active_at(time)]


class Event():
    def __init__(self, name, start=None, duration=None, location_id=None):
        self.name = name
        self.start = parser.parse(start)
        self.duration = timedelta(minutes=duration)
        self.location_id = location_id

    @property
    def finish(self):
        return self.start + self.duration

    def active_at(self, now):
        now = parser.parse(now)
        return (now >= self.start and now < self.finish)


class Location():
    def __init__(self, name):
        self.name = name
