from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_

from calendarevents import model
from calendarevents.model import DBSession
from pylons import tmpl_context

from tgext.pluggable import plug_redirect
from tgext.datahelpers.validators import SQLAEntityConverter
from tgext.datahelpers.utils import fail_with

from calendarevents.lib import get_form

class CalendarController(TGController):
    @expose('calendarevents.templates.calendar')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
            error_handler=fail_with(404))
    def _default(self, cal):
        return dict(cal=cal.view_events())

    @expose('calendarevents.templates.newevent')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(403))
    def newevent(self, cal, **kw):
        if isinstance(cal, basestring):
            cal = SQLAEntityConverter(model.Calendar).to_python(cal)
        return dict(cal=cal, form=get_form())

    @expose()
    @validate(get_form(), error_handler=newevent)
    def addevent(self, cal, **kw):
        print kw
        flash(_('Event successfully added'))
        return plug_redirect('calendarevents', '/calendar/%s' % cal)


"""
    @expose('calendarevents.templates.addevent')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
            error_handler=fail_with(404))
    @validate(form=new_event_form,
            error_handler=fail_with(404))
    def addevent(self, cal):
        pass

"""