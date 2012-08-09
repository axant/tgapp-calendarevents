from tg import expose
from calendarevents import model
from calendarevents.model import DBSession


@expose('calendarevents.templates.partials.event')
def event(self, event):
    return dict(calendar_event=event)