from django.conf.urls.defaults import patterns, include, url
from piston.resource import Resource
from frontend.api.authentication import DjangoAuthentication
from frontend.api.handlers import EventHandler, StatusHandler, VoteHandler

django_auth = DjangoAuthentication()

events = Resource(handler=EventHandler, authentication=django_auth)
statuses = Resource(handler=StatusHandler, authentication=django_auth)
votes = Resource(handler=VoteHandler, authentication=django_auth)

urlpatterns = patterns('frontend.api.views',
    url(r'^events/(?P<id>\d+)/$', events),
    url(r'^events/(?P<event_id>\d+)/statuses/$', statuses),
    url(r'^events/(?P<event_id>\d+)/votes/$', votes),
)
