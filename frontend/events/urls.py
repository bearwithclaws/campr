from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frontend.events.views',
    url(r'^(?P<event_id>\d+)$', 'dashboard'),
)
