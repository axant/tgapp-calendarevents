from datetime import timedelta
from calendarevents import model
from calendarevents.model import CalendarEvent


def create_calendar(name, events_type):
    new_calendar = model.Calendar(name=name, events_type=events_type)
    model.DBSession.add(new_calendar)
    return new_calendar


def create_event(cal, name, summary, datetime, location, linked_entity_type, linked_entity_id, end_time=None):
    new_event = CalendarEvent(calendar_id=cal.uid, name=name,
                              summary=summary, datetime=datetime,
                              end_time=end_time,
                              location=location,
                              linked_entity_type=linked_entity_type,
                              linked_entity_id=linked_entity_id)
    model.DBSession.add(new_event)
    return new_event


def get_event(event_id):

    return model.DBSession.query(model.CalendarEvent).get(event_id)


def get_calendar_events_from_datetime(calendar, datetime):

    return model.DBSession.query(CalendarEvent).filter(CalendarEvent.datetime >= datetime)\
        .filter(CalendarEvent.calendar_id == calendar)


def get_calendar_day_events(calendar, start_time):
    start_time = start_time.replace(hour=0, minute=0, second=0, microsecond=0)
    end_time = start_time + timedelta(days=1)
    return model.DBSession.query(CalendarEvent).filter(CalendarEvent.datetime >= start_time ) \
            .filter(CalendarEvent.datetime < end_time) \
            .filter(CalendarEvent.calendar_id == calendar)