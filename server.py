#! /usr/bin/env python

import os
import os.path as op
#import tornado.httpserver
import tornado.ioloop
import tornado.wsgi
import tornadio.server
import sys
import django.core.handlers.wsgi
from chat.chatroom import ChatRouter

ROOT = op.normpath(op.dirname(__file__))
def main(port):
    # Starting Django
    sys.path.append(op.join(ROOT, 'frontend'))
    os.environ['DJANGO_SETTINGS_MODULE'] = 'frontend.settings'

    wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    tornado_app = tornado.web.Application(
        [
            (r'/', tornado.web.FallbackHandler, {'fallback': wsgi_app}),
            (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': op.join(ROOT, 'frontend/static')}),
            ChatRouter.route(),
            (r'.*', tornado.web.FallbackHandler, {'fallback': wsgi_app}),
        ],
        flash_policy_port = 843,
        flash_policy_file = op.join(ROOT, 'flashpolicy.xml'),
        socket_io_port=port
    )

    io_loop = tornado.ioloop.IOLoop.instance()
    tornadio.server.SocketServer(tornado_app, io_loop=io_loop)
    io_loop.start()


if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', help='Specify the socket IO port')
    (options, args) = parser.parse_args()

    main(options.port)
