from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from calendarevents.model import DeclarativeBase
from calendarevents.model import DBSession
from tgext.pluggable import app_model, primary_key
from datetime import datetime
from datetime import timedelta
import pywapi

class Calendar(DeclarativeBase):
    __tablename__ = 'calendarevents_calendar'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(64))

    def view_events(self):
        events = DBSession.query(CalendarEvent).filter_by(calendar_id=self.uid).all()
        for event in events:
            return event.view_event_details()

class CalendarEvent(DeclarativeBase):
    __tablename__ = 'calendarevents_event'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    summary = Column(Unicode(1024))
    date = Column(DateTime, nullable=False)
    location = Column(Unicode(255), nullable=False)

    calendar_id = Column(Integer, ForeignKey(Calendar.uid), nullable=False)
    calendar =  relation(Calendar, backref=backref('events', cascade='all, delete-orphan'))

    def view_event_details(self):
        weather = pywapi.get_weather_from_google(self.location, hl='it')
        delta = datetime.now() - self.date
        today_to_event = timedelta(seconds=delta.seconds)
        if datetime.now() < self.date and today_to_event.days < 1:
            weather = weather['current_condition']['conditions']
        elif datetime.now() < self.date and today_to_event.days < 5:
            weather = weather['forecasts'][today_to_event.days]['conditions']
        else:
            weather = "Weather conditions not available"
            
        
        
        
        return weather
