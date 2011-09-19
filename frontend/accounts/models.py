from django.db import models
from django.contrib.auth.models import User
import tweepy
from frontend.events.models import Checkin, Event, Message
from django.db.models.signals import post_save

class UserProfile(models.Model):
    user = models.OneToOneField(User)

    def profile_image_url(self):
        twitter_user = tweepy.api.get_user(self.user.username)
        return twitter_user.profile_image_url.replace('_normal', '_bigger');

    def latest_message(self):
        # TODO Find event from request/session/context
        # event = Event.objects.filter(user=self.user.id).latest('time')

        checkin = Checkin.objects.filter(user=self.user.id).latest('time')
        latest_message = Message.objects.filter(checkin=checkin.id).latest('time')

        return latest_message.message

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
