from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

def index(request):
    event_id = '1001';
    user = 'calum'
    return render_to_response(
        'app/index.html',
        {'update_status_action': '/api/'+event_id+'/status',
         'user': user},
        context_instance=RequestContext(request))
