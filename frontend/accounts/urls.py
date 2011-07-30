from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frontend.app.views',
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
)
