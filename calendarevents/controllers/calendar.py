from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.i18n import ugettext as _, lazy_ugettext as l_

from calendarevents import model
from calendarevents.model import DBSession
from pylons import tmpl_context

from tgext.pluggable import plug_redirect
from tgext.datahelpers.validators import SQLAEntityConverter
from tgext.datahelpers.utils import fail_with, object_primary_key

from calendarevents.lib import get_form

class CalendarController(TGController):
    @expose('calendarevents.templates.calendar')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
            error_handler=fail_with(404))
    def _default(self, cal):
        return dict(cal=cal.view_events(), calendar=cal)

    @expose('calendarevents.templates.newevent')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(403))
    def newevent(self, cal, **kw):
        if isinstance(cal, basestring):
            cal = SQLAEntityConverter(model.Calendar).to_python(cal)

        linkable_entity_config = config['_calendarevents']['entities'][cal.associated_resources]
        linkable_entity_class, linkable_entity_field, notused = linkable_entity_config

        linkable_entities = DBSession.query(linkable_entity_class)
        linkable_entities = [(getattr(e, object_primary_key(e)),
                              getattr(e, linkable_entity_field)) for e in linkable_entities]
        return dict(cal=cal, form=get_form(), linkable_entities=linkable_entities)

    @expose()
    @validate(get_form(), error_handler=newevent)
    def addevent(self, cal, **kw):
        new_event = model.CalendarEvent(calendar_id=cal.uid, name=kw['name'],
                                        summary=kw['summary'], datetime=kw['datetime'],
                                        location=kw['location'],
                                        linked_entity_type=cal.associated_resources,
                                        linked_entity_id=kw.get('linked_entity'))
        try:
            model.DBSession.add(new_event)
            flash(_('Event successfully added'))
        except:
            flash(_('There was a problem adding your event'))
        return plug_redirect('calendarevents', '/calendar/%s' % cal.uid)

