from django.db import models
from django.contrib.auth.models import User
import tweepy
try:
    from events.signals import *
except:
    pass


class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=250)
    slug = models.SlugField()

    def __unicode__(self):
        return self.name


class Checkin(models.Model):
    event = models.ForeignKey(Event)
    user = models.ForeignKey(User)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username, self.event.name)

    def profile_image_url(self):
        twitter_user = tweepy.api.get_user(self.user.username)
        return twitter_user.profile_image_url.replace('_normal', '_bigger');

    def latest_message(self):
        latest_message = Message.objects.filter(checkin=self.id).latest('time')
        return latest_message.message


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
