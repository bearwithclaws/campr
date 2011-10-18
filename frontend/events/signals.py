from django.conf import settings
from django.core import serializers
from django.db.models.signals import post_save
from django.dispatch import receiver
import pika
from events.models import Message

@receiver(post_save, sender=Message)
def on_status_received(sender, instance, created, **kwargs):
    connection = pika.BlockingConnection(pika.ConnectionParameters(**settings.RABBITMQ_CONN))
    channel = connection.channel()
    channel.queue_declare(queue=settings.RABBITMQ_QUEUE_NAME)

    data = serializers.serialize('json', [instance])
    channel.basic_publish(exchange='', routing_key='hello', body=data)
    print ' [x] Data sent to queue: {0}'.format(data)
    connection.close()

