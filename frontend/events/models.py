from django.db import models
from django.contrib.auth.models import User
try:
    from events.signals import *
except:
    pass


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Checkin(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username, self.event.name)


class Message(models.Model):
    checkin = models.ForeignKey(Checkin)
    message = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}: {1} - {2}".format(self.checkin.user.username, self.checkin.event.name, self.message)


class Vote(models.Model):
    checkin = models.ForeignKey(Checkin)
    recipient = models.ForeignKey(User, related_name='recipients')
    voter = models.ForeignKey(User, related_name='voters')

    def __unicode__(self):
        return "{0}: {1} > {2}".format(self.checkin.event.name, self.voter.username, self.recipient.username)
