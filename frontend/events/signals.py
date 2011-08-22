from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from events.models import Status, Vote

@receiver(post_save, sender=Status)
def on_status_received(sender, instance, created, **kwargs):
    print ' [x] Status received - {0}: {1}'.format(
            settings.RABBITMQ_QUEUE_NAME, instance.message)

@receiver(post_save, sender=Vote)
def on_vote_received(sender, instance, created, **kwargs):
    print ' [x] Vote received'
