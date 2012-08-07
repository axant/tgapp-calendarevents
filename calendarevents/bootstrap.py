# -*- coding: utf-8 -*-
"""Setup the calendarevents application"""

from calendarevents import model
from tgext.pluggable import app_model
from datetime import datetime

def bootstrap(command, conf, vars):
    print 'Bootstrapping calendarevents...'

    g = app_model.Group(group_name='calendarevents', display_name='Calendar Events manager')
    model.DBSession.add(g)
    model.DBSession.flush()

    u1 = model.DBSession.query(app_model.User).filter_by(user_name='manager').first()
    if u1:
        g.users.append(u1)

    c = model.DBSession.query(model.Calendar).first()
    if not c:
        c = model.Calendar(name='default')
        model.DBSession.add(c)

    e = model.DBSession.query(model.CalendarEvent).first()
    if not e:
        e = model.CalendarEvent(calendar_id=c.uid,name='default_event', summary='default_description', date=datetime.now(), location='torino,it')
        model.DBSession.add(e)

    model.DBSession.flush()

