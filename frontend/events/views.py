from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext
from social_auth import __version__ as version
from frontend.events.models import Event

# Create your views here.
@login_required
def dashboard(request, event_id):
    """Login complete view, displays user data"""

    event = Event.objects.get(id=event_id)

    ctx = {'accounts': request.user.social_auth.all(),
           'version': version,
           'last_login': request.session.get('social_auth_last_login_backend'),
           'username': request.user.username,
           'event': event,
           }
    return render_to_response('events/dashboard.html', ctx, RequestContext(request))

