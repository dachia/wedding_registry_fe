from django.conf.urls import *
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('registry_app.views',
    (r'^$', 'index'),
    (r'^add_wish$', 'add_wish')
)
