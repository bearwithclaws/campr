from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frontend.app.views',
    url(r'^(?<event_id>\d+)$', 'dashboard'),
)
