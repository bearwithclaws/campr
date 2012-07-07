from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.events.views',
    url(r'^(?P<event_id>\d+)/$', 'index'),
    url(r'^(?P<slug>[-\w]+)/$', 'index'),
    url(r'^(?P<event_id>\d+)/checkin$', 'checkin'),
    url(r'^(?P<slug>[-\w]+)/checkin$', 'checkin'),
)
