import datetime
from calendarevents import model

def create_calendar(name, events_type):
    new_calendar = model.Calendar(name=name, events_type=events_type)
    model.DBSession.add(new_calendar)
    return new_calendar


def create_event(cal, name, summary, datetime, location, linked_entity_type, linked_entity_id, end_time=None):
    new_event = model.CalendarEvent(calendar_id=cal.uid, name=name,
                                    summary=summary, datetime=datetime,
                                    end_time=end_time,
                                    location=location,
                                    linked_entity_type=linked_entity_type,
                                    linked_entity_id=linked_entity_id)
    model.DBSession.add(new_event)
    return new_event


def get_event(event_id):
    return model.DBSession.query(model.CalendarEvent).get(event_id)