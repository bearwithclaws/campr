from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name

class Checkin(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

class Status(models.Model):
    checkin = models.ForeignKey(Checkin)
    message = models.CharField(max_length=140)

    class Meta:
        verbose_name_plural = 'statuses'

class Vote(models.Model):
    event = models.ForeignKey(Event)
    recipient = models.ForeignKey(User, related_name='recipients')
    voter = models.ForeignKey(User, related_name='voters')
