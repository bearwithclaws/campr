from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Max, F
from piston.handler import BaseHandler
from piston.utils import rc

from frontend.events.models import Event, Message, Checkin

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

class MessageHandler(BaseHandler):
    model = Message
    fields = ('message', 'time', ('checkin', ('user_id', )), )

    def read(self, request, *args, **kwargs):
        qs = self.queryset(request)

        if 'event_id' not in kwargs:
            return rc.NOT_FOUND
        event_id = kwargs['event_id']

        return qs.filter(checkin__event=event_id) \
                .annotate(last_update=Max('checkin__message__time')) \
                .filter(time=F('last_update'))

    def create(self, request, event_id):
        if not hasattr(request, "data"):
            request.data = request.POST

        attrs = self.flatten_dict(request.data)
        message = Message(checkin=Checkin.objects.get(user=request.user.id, event=event_id),
                          message=attrs['message'])
        message.save()
        return message
