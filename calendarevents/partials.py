from datetime import datetime
import json
from tg import expose, validate
import tg
from tgext.datahelpers.utils import fail_with
from tgext.datahelpers.validators import SQLAEntityConverter
from calendarevents import model
from calendarevents.model import DBSession


@expose('calendarevents.templates.partials.event')
def event(event):
    return dict(calendar_event=event)

@validate(dict(cal=SQLAEntityConverter(model.Calendar)),
          error_handler=fail_with(404))
@expose('calendarevents.templates.partials.calendar')
def calendar(cal, start_from=datetime.utcnow(), view='month', all_day_slot=False, slot_minutes=15, first_hour=8):
    events = {'values': [e.calendar_data for e in cal.events]}
    if view not in ('month', 'basicWeek', 'basicDay', 'agendaWeek', 'agendaDay'):
        view = 'month'

    for res in cal.events_type_info.resources:
        res.inject()

    return dict(cal=cal, events=tg.json_encode(events), start_from=start_from, view=view,
                all_day_slot=all_day_slot,  slot_minutes=slot_minutes, first_hour=first_hour)