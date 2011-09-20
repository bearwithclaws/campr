from django.shortcuts import render_to_response
from django.template import RequestContext
from frontend.events.models import Event

def index(request):
    ctx = {
        'events': Event.objects.all(),
    }
    return render_to_response('app/index.html', ctx, RequestContext(request))

