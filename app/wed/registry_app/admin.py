from django.contrib import admin
from registry_app.models import Item, Event, UserEvent


admin.site.register(Item)
admin.site.register(Event)
admin.site.register(UserEvent)