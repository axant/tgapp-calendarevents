# -*- coding: utf-8 -*-
"""The tgapp-calendarevents package"""

from tg import config
from calendarevents import model

def plugme(app_config, options):
    config['_calendarevents'] = options
    return dict(appid='calendarevents', global_helpers=False)

