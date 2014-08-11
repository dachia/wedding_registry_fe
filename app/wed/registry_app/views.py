from django.http import HttpResponse, HttpResponseRedirect, HttpResponseServerError
from django.template import Context, loader, Template, RequestContext
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login



@login_required
def index(request):
    return render_to_response("layout.html")
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login")