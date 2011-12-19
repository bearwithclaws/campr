#! /usr/bin/env python
import os
import os.path as op
import signal
import pika
from pika.adapters.tornado_connection import TornadoConnection
import tornado.ioloop
import tornado.web
import tornadio
import tornadio.router
import tornadio.server
from lib.observer import Observable
import django.core.handlers.wsgi
from urlparse import urlparse
from django.conf import settings

ROOT = op.normpath(op.join(op.dirname(__file__), '../'))

class ChatConnection(tornadio.SocketConnection):
    # Class level variable
    participants = set()

    def on_open(self, *args, **kwargs):
        self.participants.add(self)

    def on_message(self, message):
        self.send_message(message)

    def on_close(self):
        self.participants.remove(self)

    def send_message(self, message):
        for p in self.participants:
            p.send(message)


class PikaClient(Observable):
    def __init__(self):
        Observable.__init__(self)

        self.queue_name = settings.RABBITMQ_QUEUE_NAME

        # States
        self.connected = False
        self.connecting = False

        # Resources
        self.connection = None
        self.channel = None

        # Message caches
        self.messages = list()

    # amqp://uname:pwd@host.heroku.srs.rabbitmq.com:13029/vhost
    def connection_parameters(self):
        connection_parameters = settings.RABBITMQ_CONN

        if ('RABBITMQ_URL' in os.environ):
            rabbitmq_url = urlparse(os.environ['RABBITMQ_URL'])

            connection_parameters = {'host': rabbitmq_url.hostname}
            if rabbitmq_url.port:
                connection_parameters['port'] = rabbitmq_url.port
            if rabbitmq_url.username:
                connection_parameters['credentials'] = pika.PlainCredentials(
                    rabbitmq_url.username,
                    rabbitmq_url.password)
            if rabbitmq_url.path:
                connection_parameters['virtual_host'] = rabbitmq_url.path

        return connection_parameters

    def connect(self):
        if self.connecting:
            pika.log.info('Already connecting to RabbitMQ')
            return
        pika.log.info('Connecting to RabbitMQ')
        self.connecting = True

        connection_parameters = self.connection_parameters()
        param = pika.ConnectionParameters(**connection_parameters)

        self.connection = TornadoConnection(param,
                on_open_callback=self.on_connected)

        self.connection.add_on_close_callback(self.on_closed)

    def on_connected(self, connection):
        pika.log.info('Connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)

    def on_channel_open(self, channel):
        pika.log.info('Channel opened')
        self.channel = channel
        self.channel.queue_declare(queue=self.queue_name,
                callback=self.on_queue_declared)

    def on_queue_declared(self, frame):
        pika.log.info('Queue declared')
        self.channel.basic_consume(queue=self.queue_name,
                consumer_callback=self.on_message)

    def on_message(self, channel, method, header, body):
        pika.log.info('Message received: {0}'.format(body))
        self.messages.append(body)
        self.channel.basic_ack(delivery_tag=method.delivery_tag)
        self.notify()

    def on_closed(self, connection):
        tornado.ioloop.IOLoop.instance().stop()

    def get_messages(self):
        output = self.messages
        self.messages = list()
        return output


class Application():
    def __init__(self, port):
        settings = {
            'debug': True,
            'enabled_protocols': ['websocket',
                                    'flashsocket',
                                    'xhr-multipart',
                                    'xhr-polling'],
            'flash_policy_port': 843,
            'flash_policy_file': op.join(ROOT, 'flashpolicy.xml'),
            'socket_io_port': port
        }

        wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
        self.application = tornado.web.Application([
                (r'/', tornado.web.FallbackHandler, {'fallback': wsgi_app}),
                (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': op.join(ROOT, 'static')}),
                tornadio.get_router(ChatConnection).route(),
                (r'.*', tornado.web.FallbackHandler, {'fallback': wsgi_app}),
            ], **settings)

        self.message_queue = PikaClient()
        self.message_queue.attach(self)
        self.server = None

        pika.log.setup(color=True)

    def start(self):
        pika.log.info('Queue Pika to load')
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(1500, self.message_queue.connect)

        pika.log.info('Starting Tornado HTTPServer')
        tornadio.server.SocketServer(self.application, io_loop=io_loop)

    def stop(self):
        pika.log.info('Stopping server')
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(2, tornado.ioloop.IOLoop.instance().stop)

    def update(self, emitter):
        pika.log.info('Receiving update - send to {0} participants'.format(len(ChatConnection.participants)))
        messages = self.message_queue.get_messages()
        for p in ChatConnection.participants:
            for m in messages:
                p.send('{0}'.format(m))
