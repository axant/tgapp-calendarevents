# -*- coding: utf-8 -*-
"""The tgapp-calendarevents package"""
from calendarevents.lib.event_type import EventType


def plugme(app_config, options):
    app_config['_calendarevents'] = options
    return dict(appid='calendarevents', global_helpers=False)

