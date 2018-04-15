import dateutil.parser as parser
from datetime import timedelta
from right_now import Schedule, Event


def test_loading_schedule():
    schedule = Schedule('tests/basic.json')
    assert schedule


def test_loaded_schedule_events_count():
    schedule = Schedule('tests/basic.json')
    assert len(schedule.events) == 3


def test_loaded_schedule_events_start():
    schedule = Schedule('tests/basic.json')
    assert schedule.events[0].start == parser.parse('2018-06-01T14:00:00Z')


def test_loaded_schedule_events_duration():
    schedule = Schedule('tests/basic.json')
    assert schedule.events[0].duration == timedelta(minutes=45)


def test_loaded_schedule_events_finish():
    schedule = Schedule('tests/basic.json')
    assert schedule.events[0].finish == parser.parse('2018-06-01T14:45:00Z')
    assert schedule.events[1].finish == parser.parse('2018-06-01T16:00:00Z')


def test_event_is_active_inclusive_start_exclusive_finish():
    event = Event('Test', "2018-06-01T14:00:00Z", 45)
    assert event.active_at("2018-05-01T14:05:00Z") == False
    assert event.active_at("2018-06-01T13:59:59Z") == False
    assert event.active_at("2018-06-01T14:00:00Z") == True
    assert event.active_at("2018-06-01T14:30:00Z") == True
    assert event.active_at("2018-06-01T14:45:00Z") == False
    assert event.active_at("2018-06-01T14:45:01Z") == False
