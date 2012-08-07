from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from calendarevents.model import DeclarativeBase
from tgext.pluggable import app_model, primary_key

class Calendar(DeclarativeBase):
    __tablename__ = 'calendarevents_calendar'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(64))

class CalendarEvent(DeclarativeBase):
    __tablename__ = 'calendarevents_event'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(255))
    summary = Column(Unicode(1024))

    calendar_id = Column(Integer, ForeignKey(Calendar.uid), nullable=False)
    calendar =  relation(Calendar, backref=backref('events', cascade='all, delete-orphan'))



