from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

class Status(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = 'statuses'

    def __unicode__(self):
        return '{0} - [{1}] {2}'.format(self.event, self.time, self.message)

class Vote(models.Model):
    event = models.ForeignKey(Event)
    recipient = models.ForeignKey(User, related_name='recipients')
    voter = models.ForeignKey(User, related_name='voters')
