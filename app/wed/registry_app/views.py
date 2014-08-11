from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, loader, Template, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from registry_app import models


def index(request):
    return render_to_response("layout.html")


def wishes(request):
    """Manage wish items and stuff"""
    events = models.Event.objects.all()
    items = events[0].article_set.all()
    return render_to_response("wishlist/wish.html", {"events": events, "items": items}, RequestContext(request))


def wish(request, id=None):
    """Manage wish items and stuff"""

    events = models.Event.objects.all()
    if id:
        items = models.Event.objects.get(id=id).item_set.all()
    else:
        items = events[0].item_set.all()

    return render_to_response("wishlist/wish.html", {"events": events, "items": items}, RequestContext(request))
