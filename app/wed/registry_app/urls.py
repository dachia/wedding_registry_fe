from django.conf.urls import *
from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()


urlpatterns = patterns('registry_app.views',
    (r'^$', 'index'),
    (r'^wish$', 'wish'),
    (r'^wish/(?P<id>[0-9]+)/$', 'wish'),
    (r'^logout_view', 'logout_view'),
)
