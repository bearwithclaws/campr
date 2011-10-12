from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from social_auth import __version__ as version

# Create your views here.
def login(request):
    """Logs in user"""
    nextParam = request.GET.get('next', '')
    return render_to_response('accounts/login.html',
        {'next': nextParam}, RequestContext(request))

def error(request):
    """Error view"""
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    return render_to_response('accounts/error.html', {'version': version,
                                             'error_msg': error_msg},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')
