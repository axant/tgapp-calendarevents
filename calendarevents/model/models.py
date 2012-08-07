from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from calendarevents.model import DeclarativeBase
from calendarevents.model import DBSession
from tgext.pluggable import app_model, primary_key
from datetime import datetime
from datetime import timedelta
import pywapi, re

location_regular_expression = re.compile(r"([a-z]+,[a-z]{2})")

class Event:
	def __init__(self):
		self.name = ''
		self.summary = ''
		self.datetime = datetime(2000,01,01)
		self.location = ''
		self.weather = ''

class Calendar(DeclarativeBase):
    __tablename__ = 'calendarevents_calendar'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(64))

    def view_events(self):
        events = DBSession.query(CalendarEvent).filter_by(calendar_id=self.uid).all()
        events_list = []
        for event in events:
            events_list.append(event.event_details())
        return events_list

    def add_event(self, name, datetime, summary, location):
        if location_regular_expression.match(location):
            if datetime > datetime.now():
                new_event = CalendarEvent(calendar_id=self.uid,name=name, summary=summary, datetime=datetime, location=location)
                DBSession.add(new_event)
        
        
class CalendarEvent(DeclarativeBase):
    __tablename__ = 'calendarevents_event'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(255), nullable=False)
    summary = Column(Unicode(1024))
    datetime = Column(DateTime, nullable=False)
    location = Column(Unicode(255), nullable=False)

    calendar_id = Column(Integer, ForeignKey(Calendar.uid), nullable=False)
    calendar = relation(Calendar, backref=backref('events', cascade='all, delete-orphan'))

    def event_details(self):
        this_event = Event()
        this_event.name = self.name
        this_event.summary = self.summary
        this_event.datetime = self.datetime
        this_event.location = self.location
        this_event.weather = "Weather conditions not available"
        today_to_event = self.datetime - datetime.now()
        today_to_event = timedelta(seconds=today_to_event.seconds)
        if datetime.now() < self.datetime:
            weather = pywapi.get_weather_from_google(self.location, hl='it')
            if today_to_event.days < 1:
                this_event.weather = weather['current_conditions']['condition']
            elif today_to_event.days < 5:
                this_event.weather = weather['forecasts'][today_to_event.days]['condition']
        return this_event

