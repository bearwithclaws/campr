from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'frontend.app.views.index', name='home'),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('frontend.accounts.urls')),
    url(r'^events/', include('frontend.events.urls')),
    url(r'', include('frontend.app.urls')),
    url(r'', include('social_auth.urls')),

    # Examples:
    # url(r'^$', 'frontend.views.home', name='home'),
    # url(r'^frontend/', include('frontend.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
)
