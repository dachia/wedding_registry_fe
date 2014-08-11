from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, loader, Template, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render_to_response("layout.html")
