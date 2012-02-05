"""
This module contains classes that contribute to the Campr class, which
is a tornado app that handles all of Campr's functionality.
"""
import os
import tornadio
import tornadio.router
import tornadio.server
import tornado.ioloop
import tornado.web

class HomeHandler(tornado.web.RequestHandler):
    """
    Handles basic homepage HTTP requests.
    """
    def get(self):
        self.render("templates/index.html", title="Home")


class CamprConnection(tornadio.SocketConnection):
    """
    The Campr socket connection class. Its methods define what we
    do when different kinds of events come in over the socket.
    """
    participants = set()

    def on_open(self, *args, **kwargs):
        """
        Handles when we get a new connection in over socket.IO
        """
        self.participants.add(self)

    def on_message(self, message):
        """
        Handles when we receive a new message from a participant over socket.IO
        """
        for p in self.participants:
            p.send('{0}'.format(message))

    def on_close(self):
        """
        What to do when a participant's connection closes.
        """
        self.participants.remove(self)


class Campr():
    """
    The Campr tornado application.
    """
    def __init__(self):
        """
        Constructor. Currently takes not arguments.
        """
        settings = {
            "static_path": os.path.join(os.path.dirname(__file__), "static"),
            "socket_io_port": 8888,
            'flash_policy_port': 843,
            'enabled_protocols': ['websocket',
                                  'flashsocket',
                                  'xhr-multipart',
                                  'xhr-polling'],
        }
        self.application = tornado.web.Application([
                (r"/", HomeHandler),
                tornadio.get_router(CamprConnection).route(),
            ], **settings)
        self.server = None

    def start(self):
        """
        Starts the Campr tornado app.
        """
        io_loop = tornado.ioloop.IOLoop.instance()
        tornadio.server.SocketServer(self.application, io_loop=io_loop)

    def stop(self):
        """
        Stops the Campr tornado app.
        """
        io_loop = tornado.ioloop.IOLoop.instance()
        io_loop.add_timeout(2, tornado.ioloop.IOLoop.instance().stop)
