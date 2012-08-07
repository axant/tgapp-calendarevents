from tg import expose

@expose('calendarevents.templates.little_partial')
def something(name):
    return dict(name=name)