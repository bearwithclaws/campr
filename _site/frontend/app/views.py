from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from social_auth import __version__ as version

def index(request):
    return render_to_response('app/index.html')

@login_required
def dashboard(request):
    """Login complete view, displays user data"""
    ctx = {'accounts': request.user.social_auth.all(),
           'version': version,
           'last_login': request.session.get('social_auth_last_login_backend')
           }
    return render_to_response('done.html', ctx, RequestContext(request))

#def error(request):
#    """Error view"""
#    error_msg = request.session.pop(settings.SOCIAL_AUTH_ERROR_KEY, None)
#    return render_to_response('error.html', {'version': version,
#                                             'error_msg': error_msg},
#                              RequestContext(request))

#def logout(request):
#    """Logs out user"""
#    auth_logout(request)
#    return HttpResponseRedirect('/')
