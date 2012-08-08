# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_

from calendarevents import model
from calendarevents.model import DBSession

from tgext.pluggable import plug_redirect

from .calendar import CalendarController
from calendarevents.lib.forms import new_calendar_form

class RootController(TGController):
    calendar = CalendarController()

    @expose('calendarevents.templates.index')
    def index(self):
        return plug_redirect('calendarevents', '/calendarlist')

    @expose('calendarevents.templates.calendarlist')
    def calendarlist(self):
        calendar_list = DBSession.query(model.Calendar).all()
        return dict(calendar_list=calendar_list)

    @expose('calendarevents.templates.newcalendar')
    def newcalendar(self, **kw):
        return dict(form=new_calendar_form)

    @expose()
    @validate(new_calendar_form, error_handler=newcalendar)
    def addcalendar(self, name, events_type):
        new_calendar = model.Calendar(name=name, events_type=events_type)
        model.DBSession.add(new_calendar)
        model.DBSession.flush()
        flash(_('Calendar successfully added'))
        return plug_redirect('calendarevents', '/calendar/%s' % new_calendar.uid)
        