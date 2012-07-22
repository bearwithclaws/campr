from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from frontend.api.authentication import DjangoAuthentication
from frontend.api.handlers import EventHandler, MessageHandler

django_auth = DjangoAuthentication()

events = Resource(handler=EventHandler)
messages = Resource(handler=MessageHandler, authentication=django_auth)

urlpatterns = patterns('frontend.api.views',
    url(r'^events/(?P<id>\d+)/$', events),
    url(r'^events/(?P<slug>[-\w]+)/$', events),
    url(r'^events/(?P<event_id>\d+)/messages/$', messages),
)
