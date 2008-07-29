from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext

def frontpage(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/repos/manage/")
    else:
        return HttpResponseRedirect("/accounts/")

@login_required
def manage(request):
    user = request.user
    return render_to_response('you are user : '+str(user.username))

