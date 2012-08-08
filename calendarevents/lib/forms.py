from tw.api import WidgetsList
from tw.forms import TableForm, TextField, HiddenField
from tw.forms import validators
from tw.forms.calendars import CalendarDatePicker
from tgext.datahelpers.validators import SQLAEntityConverter
from tg.i18n import lazy_ugettext as l_
from calendarevents import model

class NewEventForm(TableForm):
    class fields(WidgetsList):
        cal = HiddenField(validator=SQLAEntityConverter(model.Calendar))
        name = TextField(label_text=l_('Event Name'), validator=validators.UnicodeString(not_empty=True))
        summary = TextField(label_text=l_('Event short summary'), validator=validators.UnicodeString(not_empty=True))
        datetime = CalendarDatePicker(label_text=l_('Event date'))
        location = TextField(label_text=l_('Event Location (es: turin,it)'), validator=validators.UnicodeString(not_empty=True))
