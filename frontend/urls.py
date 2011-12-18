from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'frontend.app.views.index', name='home'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/', include('frontend.accounts.urls')),
    url(r'^api/', include('frontend.api.urls')),
    url(r'^events/', include('frontend.events.urls')),
    url(r'', include('social_auth.urls')),

)
