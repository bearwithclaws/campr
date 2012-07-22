from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from social_auth import __version__ as version
from frontend.events.models import Checkin, Event
from django.shortcuts import get_object_or_404
import re

# Create your views here.
def login(request):
    """Logs in user"""

    nextParam = request.GET.get('next', '')
    ctx = { 'next': nextParam }

    # Ugh! Must be a better way...
    # Looking for string of form: '/events/1/checkin'
    matched = re.search( r'events/([-\w]+)/', nextParam )
    if matched.group(1).isdigit():
        event_id = int(matched.group(1))
        ctx['event'] = get_object_or_404(Event, id=event_id)
    elif matched.group(1):
        slug = matched.group(1)
        ctx['event'] = get_object_or_404(Event, slug=slug)

    return render_to_response('accounts/login.html',
        ctx, RequestContext(request))

def error(request):
    """Error view"""
    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
    return render_to_response('accounts/error.html', {'version': version,
                                             'error_msg': error_msg},
                              RequestContext(request))

def logout(request):
    """Logs out user"""
    checkins = Checkin.objects.filter(user=request.user.id)
    for checkin in checkins:
        checkin.present = False
        checkin.save()

    auth_logout(request)
    return HttpResponseRedirect('/')
