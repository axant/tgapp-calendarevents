import json
from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.datahelpers.utils import fail_with
from tgext.datahelpers.validators import SQLAEntityConverter

from calendarevents import model
from calendarevents.model import DBSession

from tgext.pluggable import plug_redirect

from repoze.what import predicates
from calendarevents.lib.forms import new_calendar_form

class CalendarController(TGController):
    @expose('calendarevents.templates.calendar.calendar')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(404))
    def _default(self, cal):
        events = [{'uid':e.uid, 'title':e.name, 'start':e.datetime.strftime('%Y-%m-%d %H:%M')} for e in cal.events]
        return dict(cal=cal, events=json.dumps(events))

    @expose('calendarevents.templates.calendar.events')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(404))
    def events(self, cal):
        return dict(cal=cal)

    @require(predicates.in_group('calendarevents'))
    @expose('calendarevents.templates.calendar.list')
    def list(self):
        calendar_list = DBSession.query(model.Calendar).all()
        return dict(calendar_list=calendar_list)

    @require(predicates.in_group('calendarevents'))
    @expose('calendarevents.templates.calendar.new')
    def new(self, **kw):
        return dict(form=new_calendar_form)

    @require(predicates.in_group('calendarevents'))
    @expose()
    @validate(new_calendar_form, error_handler=new)
    def save(self, name, events_type):
        new_calendar = model.Calendar(name=name, events_type=events_type)
        model.DBSession.add(new_calendar)
        model.DBSession.flush()
        flash(_('Calendar successfully added'))
        return plug_redirect('calendarevents', '/calendar/%s' % new_calendar.uid)
