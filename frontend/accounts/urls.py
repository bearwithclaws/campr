from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('frontend.accounts.views',
    url(r'^login$', 'login'),
    url(r'^logout$', 'logout'),
)
