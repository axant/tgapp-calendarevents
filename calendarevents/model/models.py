from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime
from sqlalchemy.orm import backref, relation

from calendarevents.model import DeclarativeBase
from calendarevents.model import DBSession
from datetime import datetime
import pywapi
import tg

class Calendar(DeclarativeBase):
    __tablename__ = 'calendarevents_calendar'

    uid = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(64))
    associated_resources = Column(Unicode(64))

    def view_events(self):
        events = DBSession.query(CalendarEvent).filter_by(calendar_id=self.uid).all()
        events_list = []
        for event in events:
            events_list.append(event.event_details())
        return events_list

    def add_event(self, name, datetime, summary, location):
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

    linked_entity_id = Column(Integer, nullable=False, index=True)
    linked_entity_type = Column(Unicode(255), nullable=False, index=True)


    @property
    def linked_entity_url(self):
        linked_entity_config = tg.config['_calendarevents']['entities'][self.linked_entity_type]
        linked_entity_resolver = linked_entity_config[2]
        return linked_entity_resolver(self.linked_entity_id)

    @property
    def linked_entity_title(self):
        linked_entity_config = tg.config['_calendarevents']['entities'][self.linked_entity_type]
        linked_entity_resolver = lambda b:linked_entity_config[1]
        return linked_entity_resolver(self.linked_entity_id)

    @property
    def weather(self):
        today_to_event = (self.datetime - datetime.now()).days
        weather = "Weather conditions not avaliable"
        if datetime.now() < self.datetime:
            if today_to_event < 1:
                weather = pywapi.get_weather_from_google(self.location, hl='it')
                weather = weather['current_conditions']['condition']
            elif today_to_event < 5:
                weather = pywapi.get_weather_from_google(self.location, hl='it')
                weather = weather['forecasts'][today_to_event]['condition']
        return weather
    
    
    def event_details(self):
        return self