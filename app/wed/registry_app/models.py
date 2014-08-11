from django.db import models
from django.forms import ModelForm


# Create your models here.
class Item(models.Model):
    """Wish list item entity."""
    name = models.CharField(max_length=50,
                            verbose_name="Item",
                            help_text="Enter name of wish list item here")
    link = models.URLField(blank=True)
    taken_by = models.EmailField(blank=True)
    event = models.ForeignKey("Event")

    def __unicode__(self):
        return self.name


class Event(models.Model):
    """Occasion entity."""
    time = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)

    def __unicode__(self):
        return self.title


class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ["time", "title", "description"]


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "link", "taken_by"]
