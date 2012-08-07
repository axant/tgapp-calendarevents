# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import TGController
from tg import expose, flash, require, url, lurl, request, redirect, validate
from tg.i18n import ugettext as _, lazy_ugettext as l_

from calendarevents import model
from calendarevents.model import DBSession

from tgext.pluggable import plug_redirect
from tgext.datahelpers.validators import SQLAEntityConverter
from tgext.datahelpers.utils import fail_with

class RootController(TGController):
    @expose('calendarevents.templates.index')
    def index(self):
        cal = DBSession.query(model.Calendar).first()
        return plug_redirect('calendarevents', '/calendar/%s' % cal.uid)

    @expose('calendarevents.templates.calendar')
    @validate(dict(cal=SQLAEntityConverter(model.Calendar)),
              error_handler=fail_with(404))
    def calendar(self, cal):
        return dict(cal=cal)