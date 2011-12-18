#! /usr/bin/env python

import os
import os.path as op
import signal
import tornado.ioloop
import tornado.wsgi
import tornadio.server
import sys
import django.core.handlers.wsgi
from chat.chatroom import Application

ROOT = op.normpath(op.dirname(__file__))
def main(port, rabbitmq_url):
    # Starting Django
    sys.path.append(op.join(ROOT, 'frontend'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'

    # Tornadio app part
    app = Application(port, rabbitmq_url)
    # Cleanup code
    def shutdown(sig, frame):
        app.stop()
    signal.signal(signal.SIGABRT, shutdown)
    # Once we have that, we'll start the server
    try:
        app.start()
    except KeyboardInterrupt:
        app.stop()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', help='Specify the socket IO port')
    (options, args) = parser.parse_args()

    rabbitmq_url = 'RABBITMQ_URL' in os.environ and os.environ['RABBITMQ_URL'] or 'amqp://localhost'

    main(port=options.port or 8001,
         rabbitmq_url=rabbitmq_url)
