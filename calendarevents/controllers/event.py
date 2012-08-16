from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate, config
from tg.i18n import ugettext as _, lazy_ugettext as l_

from calendarevents import model
from calendarevents.lib.forms import get_modevent_form
from calendarevents.model import DBSession

from tgext.pluggable import plug_redirect
from tgext.datahelpers.validators import SQLAEntityConverter, validated_handler
from tgext.datahelpers.utils import fail_with, object_primary_key

from calendarevents.lib import get_form
from repoze.what import predicates

class EventController(TGController):
    @expose('calendarevents.templates.event_display')
    @validate(dict(event=SQLAEntityConverter(model.CalendarEvent)),
              error_handler=fail_with(404))
    def _default(self, event):
        return dict(event=event)

    @expose('calendarevents.templates.event.newevent')
    @require(predicates.in_group('calendarevents'))
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(403))
    def new(self, cal, **kw):
        event_type = cal.events_type_info
        if not event_type:
            linkable_entities = []
        else:
            linkable_entities = event_type.get_linkable_entities(cal)
        return dict(cal=cal, form=get_form(), linkable_entities=linkable_entities)

    @require(predicates.in_group('calendarevents'))
    @expose()
    @validate(get_form(), error_handler=newevent)
    def addevent(self, cal, **kw):
        new_event = model.CalendarEvent(calendar_id=cal.uid, name=kw['name'],
                                        summary=kw['summary'], datetime=kw['datetime'],
                                        location=kw['location'],
                                        linked_entity_type=cal.events_type,
                                        linked_entity_id=kw.get('linked_entity'))
        model.DBSession.add(new_event)
        flash(_('Event successfully added'))
        return plug_redirect('calendarevents', '/calendar/%s' % cal.uid)

    @expose()
    @require(predicates.in_group('calendarevents'))
    @validate(dict(event=SQLAEntityConverter(model.CalendarEvent)),
              error_handler=fail_with(404))
    def remove(self, event):
        DBSession.delete(event)
        return redirect(request.referer)

    @require(predicates.in_group('calendarevents'))
    @expose('calendarevents.templates.calendar.modevent')
    @validate(dict(event=SQLAEntityConverter(model.CalendarEvent)),
              error_handler=fail_with(404))
    def edit(self, event, **kw):
        if isinstance(event, basestring):
            event = SQLAEntityConverter(model.CalendarEvent).to_python(event)

        cal = event.calendar
        event_type = cal.events_type_info

        if not event_type:
            linkable_entities = []
        else:
            linkable_entities = event_type.get_linkable_entities(cal)

        return dict(cal=cal, event=event, linkable_entities=linkable_entities, form=get_form())


    @require(predicates.in_group('calendarevents'))
    @expose()
    @validate(get_form(), error_handler=modevent)
    def modify_event(self, event, **kw):
        event = DBSession.query(model.CalendarEvent).get(event)
        event.name=kw['name']
        event.summary=kw['summary']
        event.datetime=kw['datetime']
        event.location=kw['location']
        event.linked_entity_id=kw.get('linked_entity')
        #DBSession.update(event)
        flash(_('Event successfully modified'))
        return plug_redirect('calendarevents', '/calendar/%s' % event.calendar_id)
