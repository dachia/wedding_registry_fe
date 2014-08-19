from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.template import Context, loader, Template, RequestContext
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login

from registry_app import models


@login_required
def index(request):
    return render_to_response("index.html")


@login_required
def wish(request, event_id=None, id=None):
    """Manage wish items and stuff"""
    Event, Form, Item = models.Event, models.ItemForm, models.Item
    event, item = get_object_or_404(Event, pk=event_id), get_object_or_404(Item, pk=id) if id else None
    go_back = redirect("/event/%s/wish" % event.id)
    action = request.GET.get("act")

    if request.method == "GET" and not action:
        form = Form(instance=item) if event else Form()

    elif request.method == "POST":
        form = Form(request.POST, instance=item) if item else Form(request.POST)
        if form.is_valid():

            if item:
                form.save()
            else:
                instance = form.save(commit=False)
                event.item_set.add(instance)

            return go_back

    elif request.method == "GET" and action == "del":
        item.delete()
        return go_back

    else:
        raise Http404

    events = Event.objects.all()
    items = event.item_set.all()

    return render_to_response("wishlist/item.html",
                              {"events": events,
                               "items": items,
                               "event_id": event.pk if event else None,
                               "item_id": item.pk if item else None,
                               "form": form
                               }, RequestContext(request))


def event(request, id=None):
    """Add event"""
    Form, Event = models.EventForm, models.Event
    event = get_object_or_404(Event, pk=id) if id else None
    go_back = redirect("/event")
    action = request.GET.get("act")

    if request.method == "GET" and not action:
        form = Form(instance=event) if event else Form()

    elif request.method == "POST":
        form = Form(request.POST, instance=event) if event else Form(request.POST)
        if form.is_valid():
            form.save()
            return go_back

    elif request.method == "GET" and action == "del":
        event.delete()
        return go_back

    else:
        raise Http404

    events = Event.objects.all()

    return render_to_response("wishlist/event.html",
                              {"form": form,
                               "event_id": event.id if event else None,
                               "events": events}, RequestContext(request))

@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")
