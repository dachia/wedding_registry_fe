import uuid
import base64

from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError, Http404
from django.template import RequestContext
from django.template.loader import render_to_string
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from keepboo_opengraph import opengraph
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from registry_app import models


@login_required
def index(request):
    return redirect("/event")


@login_required
def wish(request, event_id=None, id=None):
    """Manage wish items and stuff"""
    membership, user = get_object_or_404(models.UserEvent, event_id=event_id, user=request.user), request.user
    item = get_object_or_404(models.Item, pk=id) if id else None
    event = membership.event

    go_back = redirect("/event/%s/wish" % event.id)
    action = request.GET.get("act")

    if request.method == "GET" and not action:
        form = models.ItemForm(instance=item) if event else models.ItemForm()

    elif request.method == "POST":
        form = models.ItemForm(request.POST, instance=item) if item else models.ItemForm(request.POST)
        if form.is_valid():
            if item:
                form.save()
            else:
                instance = form.save(commit=False)
                instance.open_graph = opengraph.OpenGraph(url=instance.link)
                event.item_set.add(instance)

            return go_back

    elif request.method == "GET" and action == "del":
        item.delete()
        return go_back

    else:
        raise Http404

    memberships = user.userevent_set.all()
    items = event.item_set.all()

    return render_to_response("wishlist/item.html",
                              {"memberships": memberships,
                               "items": items,
                               "event_id": event.pk,
                               "item_id": item.pk if item else None,
                               "form": form
                               }, RequestContext(request))


@login_required
def event(request, id=None):
    """Add event"""
    membership, user = get_object_or_404(models.UserEvent, event_id=id, user=request.user) if id else None, request.user
    event = membership.event if membership else None

    go_back = redirect("/event")
    action = request.GET.get("act")

    if request.method == "GET" and not action:
        form = models.EventForm(instance=event) if event else models.EventForm()

    elif request.method == "POST" and (not membership or membership.is_owner):
        form = models.EventForm(request.POST, instance=event) if event else models.EventForm(request.POST)
        if form.is_valid():
            instance = form.save()

            if not event:
                membership = models.UserEvent(user=user,
                                       event=instance,
                                       is_owner=True)
                membership.save()

            return go_back

    elif request.method == "GET" and action == "del" and (not membership or membership.is_owner):
        event.delete()
        return go_back

    else:
        raise Http404

    memberships = user.userevent_set.all()

    return render_to_response("wishlist/event.html",
                              {"form": form,
                               "event_id": event.id if event else None,
                               "memberships": memberships}, RequestContext(request))


@login_required
def contact(request, id=None):
    """Create view edit contact"""
    user = request.user
    contact = get_object_or_404(models.Contact, id=id) if id else None
    go_back = redirect("/contact")
    action = request.GET.get("act")

    if request.method == "GET" and not action:
        form = models.ContactForm(instance=contact) if event else models.ContactForm()

    elif request.method == "POST":
        form = models.ContactForm(request.POST, instance=contact) if contact else models.ContactForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = user
            instance.save()
            return go_back
    elif request.method == "GET" and action == "del" and contact.user == user:
        contact.delete()
        return go_back
    else:
        raise Http404
    contacts = user.contact_set.all()
    return render_to_response("contact/contact.html",
                              {"form": form,
                               "contacts": contacts,
                               "contact_id": contact.id if contact else None}, RequestContext(request))


@login_required
def invite(request, event_id):
    """Invite all contacts for event_id (send emails)"""
    user, event = request.user, get_object_or_404(models.Event, id=event_id)
    contacts = user.contact_set.all()

    for contact in contacts:
        instance = models.Invite()
        instance.event = event
        instance.contact = contact
        instance.token = get_a_Uuid()
        instance.save()

        url = "http://81.81.81.6/guest/%s" % instance.token
        html_body = render_to_string("email/invite.html", {"guest_url": url})
        txt_body = render_to_string("email/invite.txt", {"guest_url": url})

        msg = EmailMultiAlternatives('Invitation', txt_body, settings.EMAIL_HOST_USER, [contact.email])
        msg.attach_alternative(html_body, "text/html")
        msg.send()

        instance.sent = True
        instance.save()

    return redirect("/event")


def get_a_Uuid():
    r_uuid = base64.urlsafe_b64encode(uuid.uuid4().bytes)
    return r_uuid.replace('=', '')


def guest(request, token):
    user = request.user

    if not user.is_anonymous():
        # add event to user
        pass
    else:
        # create a user and add him to event
        invite = get_object_or_404(models.Invite, token=token)
        if not invite.user:
            # check if user with this email exists
            user = User.objects.create_user(token, invite.contact.email, token)
            membership = models.UserEvent(user=user,
                                          event=invite.event,
                                          is_owner=False)
            membership.save()
            user = authenticate(username=token, password=token)
            login(request, user)
    return redirect("/event")


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")
