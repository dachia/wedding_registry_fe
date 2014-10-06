from django.db import models
from django.forms import ModelForm
from django.contrib.auth.models import User
from jsonfield import JSONField


# Create your models here.
class Item(models.Model):
    """Wish list item entity."""
    name = models.CharField(max_length=50,
                            verbose_name="Item",
                            help_text="Enter name of wish list item here",
                            blank=True)
    link = models.URLField(max_length=500)
    open_graph = JSONField()
    taken_by = models.EmailField(blank=True)
    event = models.ForeignKey("Event")

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """Occasion entity."""
    time = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    members = models.ManyToManyField(User, related_name="events", through="UserEvent")

    def __unicode__(self):
        return self.title


class UserEvent(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey("Event")
    is_owner = models.BooleanField(default=False)


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["time", "title", "description"]


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["link", "taken_by"]
