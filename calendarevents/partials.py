from datetime import datetime
import json
from tg import expose, validate
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
def calendar(cal, view='month', all_day_slot=False, start_from=datetime.utcnow()):
    events = [e.calendar_data for e in cal.events]
    if view not in ('month', 'basicWeek', 'basicDay', 'agendaWeek', 'agendaDay'):
        view = 'month'

    for res in cal.events_type_info.resources:
        res.inject()

    return dict(cal=cal, events=json.dumps(events), view=view, all_day_slot=all_day_slot, start_from=start_from)