from calendarevents import model


def create_calendar(name, events_type):
    new_calendar = model.Calendar(name=name, events_type=events_type)
    model.DBSession.add(new_calendar)
    return new_calendar