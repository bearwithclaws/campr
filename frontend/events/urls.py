from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('frontend.events.views',
    url(r'(?P<event_id>\d+)/$', 'dashboard'),
    url(r'(?P<event_id>\d+)/checkin$', 'checkin'),
)
