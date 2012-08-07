About calendarevents
-------------------------

calendarevents is a Pluggable application for TurboGears2.

Installing
-------------------------------

calendarevents can be installed both from pypi or from bitbucket::

    easy_install calendarevents

should just work for most of the users

Plugging calendarevents
----------------------------

In your application *config/app_cfg.py* import **plug**::

    from tgext.pluggable import plug

Then at the *end of the file* call plug with calendarevents::

    plug(base_config, 'calendarevents')

You will be able to access the registration process at
*http://localhost:8080/calendarevents*.

Available Hooks
----------------------

calendarevents makes available a some hooks which will be
called during some actions to alter the default
behavior of the appplications:

Exposed Partials
----------------------

calendarevents exposes a bunch of partials which can be used
to render pieces of the blogging system anywhere in your
application:

Exposed Templates
--------------------

The templates used by registration and that can be replaced with
*tgext.pluggable.replace_template* are:

