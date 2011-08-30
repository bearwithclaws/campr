from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from frontend.api.authentication import DjangoAuthentication
from frontend.api.handlers import EventHandler, MessageHandler, VoteHandler

django_auth = DjangoAuthentication()

events = Resource(handler=EventHandler, authentication=django_auth)
messages = Resource(handler=MessageHandler, authentication=django_auth)
votes = Resource(handler=VoteHandler, authentication=django_auth)

urlpatterns = patterns('frontend.api.views',
    url(r'^events/(?P<id>\d+)/$', events),
    url(r'^events/(?P<event_id>\d+)/messages/$', messages),
    url(r'^events/(?P<event_id>\d+)/votes/$', votes),
)
