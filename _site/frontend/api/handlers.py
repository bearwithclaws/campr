from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, F
from piston.handler import BaseHandler
from piston.utils import rc, require_mime, require_extended
from piston.utils import validate

from frontend.events.models import Event, Status, Vote

class EventHandler(BaseHandler):
    model = Event

    def read(self, request, *args, **kwargs):
        qs = self.queryset(request)
        if args != () or kwargs != {}:
            try:
                return qs.get(*args, **kwargs)
            except ObjectDoesNotExist:
                return rc.NOT_FOUND
            except MultipleObjectsReturned: # should never happen, since we're using a PK
                return rc.BAD_REQUEST
        else:
            return qs

class StatusHandler(BaseHandler):
    model = Status
    fields = ('message', 'time', ('user', ('username', 'id')))

    def read(self, request, *args, **kwargs):
        qs = self.queryset(request)
        return qs.filter(*args, **kwargs) \
                .annotate(last_update=Max('user__status__time')) \
                .filter(time=F('last_update'))

    def create(self, request, event_id):
        if not hasattr(request, "data"):
            request.data = request.POST

        attrs = self.flatten_dict(request.data)
        status = Status(event=Event.objects.get(id=event_id),
                        user=request.user,
                        message=attrs['message'])
        status.save()
        return status

class VoteHandler(BaseHandler):
    model = Vote

    def read(self, request, *args, **kwargs):
        qs = self.queryset(request)
        return qs.filter(*args, **kwargs)

    def create(self, request):
        if not hasattr(request, "data"):
            request.data = request.POST

        attrs = self.flatten_dict(request.data)

        vote = Vote(event=attrs['event'],
                    voter=request.user,
                    recipient=attrs['recipient'])
        vote.save()
        return vote
