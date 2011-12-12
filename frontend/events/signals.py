from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
import pika
from events.models import Message, Checkin
from django.utils import simplejson

def publish(data):
    connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBITMQ_CONN))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

    channel.basic_publish(exchange='', routing_key='hello', body=data)
    print ' [x] Data sent to queue: {0}'.format(data)
    connection.close()

@receiver(post_save, sender=Message)
def on_status_received(sender, instance, created, **kwargs):
    status_info = {
        'status': {
            'checkin_id': instance.checkin.id,
            'message':    instance.message,
        },
    }
    publish(simplejson.dumps(status_info))

@receiver(post_save, sender=Checkin)
def on_checkin_received(sender, instance, created, **kwargs):
    checkin_info = {
        'checkin': {
            'id':                instance.id,
            'username':          instance.user.username,
            'profile_image_url': instance.profile_image_url(),
            'present':           instance.present,
            'latest_message':    instance.latest_message(),
        },
    }
    publish(simplejson.dumps(checkin_info))
