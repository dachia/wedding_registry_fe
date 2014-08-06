__author__ = 'aleksejklebanskij'
from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('registry_app.views',
    (r'^$', 'index'),
)