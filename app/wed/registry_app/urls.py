from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()


urlpatterns = patterns('registry_app.views',
    (r'^$', 'index'),
    (r'^event/$', 'event'),
    (r'^event/(?P<id>[0-9]+)$', 'event'),
    (r'^event/(?P<event_id>[0-9]+)/invite/$', 'invite'),
    (r'^contact/$', 'contact'),
    (r'^contact/(?P<id>[0-9]+)$', 'contact'),
    (r'^event/(?P<event_id>[0-9]+)/wish/$', 'wish'),
    (r'^event/(?P<event_id>[0-9]+)/wish/(?P<id>[0-9]+)$', 'wish'),
    (r'^guest/(?P<token>[a-zA-Z0-9_\-]+)$', 'guest'),
    (r'^logout_view', 'logout_view'),
)
