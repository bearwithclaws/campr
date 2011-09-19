from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from frontend.events.models import Event, Checkin, Message

import tweepy

# Create your views here.
def dashboard(request, event_id):
    """Login complete view, displays user data"""

    event = get_object_or_404(Event, id=event_id)
    user = request.user
    checkin = Checkin.objects.filter(user=user.id, event=event.id)[0]
    status = Message.objects.filter(checkin=checkin.id).latest('time')

    twitter_user = tweepy.api.get_user(user.username)

    #TODO: Get list of users who are checked in the same event and their latest
    #      status

    # TODO: Have two different templates here: one for logged in, another one
    #       for logged out
    ctx = {
        'accounts': request.user.social_auth.all(),
        'last_login': request.session.get('social_auth_last_login_backend'),
        'user': user,
        'event': event,
        'status': status,
        'profile_image_url': twitter_user.profile_image_url.replace('_normal', '_bigger'),
    }
    return render_to_response('events/dashboard_loggedin.html', ctx, RequestContext(request))

@login_required
def checkin(request, event_id):
    """Checks-in to the event"""
    event = get_object_or_404(Event, id=event_id)
    user = request.user

    checkin, created = Checkin.objects.get_or_create(event=event, user=user)

    return redirect(dashboard, event_id=event_id)
