import json
from datetime import timedelta
import dateutil.parser as parser


class Schedule():
    def __init__(self, filename):
        self.filename = filename
        self.events = []
        self.load()

    def load(self):
        raw = json.load(open(self.filename))
        self.events = [Event(event['name'],
                       start=event['start'],
                       duration=event['duration'])
                       for event in raw['events']]


class Event():
    def __init__(self, name, start=None, duration=None):
        self.name = name
        self.start = parser.parse(start)
        self.duration = timedelta(minutes=duration)

    @property
    def finish(self):
        return self.start + self.duration

    def active_at(self, now):
        now = parser.parse(now)
        return (now >= self.start and now < self.finish)
