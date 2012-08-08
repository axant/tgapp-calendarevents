from tw.api import WidgetsList
from tw.forms import TableForm, TextField, HiddenField
from tw.forms import validators
from tgext.datahelpers.validators import SQLAEntityConverter
from tg.i18n import lazy_ugettext as l_
from calendarevents import model

class NewEventForm(TableForm):
    class fields(WidgetsList):
        cal = HiddenField(validator=SQLAEntityConverter(model.Calendar))
        name = TextField(label_text=l_('Event Name'), validator=validators.UnicodeString(not_empty=True))
