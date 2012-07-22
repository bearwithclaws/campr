from django.db import models
from django.contrib.auth.models import User
import tweepy

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
    present = models.BooleanField(default=True)

    def __unicode__(self):
        return "{0}: {1}".format(self.user.username, self.event.name)

    def profile_image_url(self):
        image_url = '/static/images/profile_image.jpg'
        try:
            twitter_user = tweepy.api.get_user(self.user.username)
            image_url = twitter_user.profile_image_url.replace('_normal', '_bigger');
        except tweepy.TweepError:
            pass
        return image_url;

    def latest_message(self):
        try:
            latest_message = Message.objects.filter(checkin=self.id).latest('time').message
        except Message.DoesNotExist:
            latest_message = "Well, I haven't updated my status yet."
        return latest_message


class Message(models.Model):
    checkin = models.ForeignKey(Checkin)
    message = models.CharField(max_length=140)
    time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "{0}: {1} - {2}".format(self.checkin.user.username, self.checkin.event.name, self.message)
