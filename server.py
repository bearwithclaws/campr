#! /usr/bin/env python
"""
The server that starts (and stops) the Campr app.
"""
import signal
from campr import Campr

if __name__ == "__main__":
    from optparse import OptionParser

    parser = OptionParser()
    parser.add_option('-p', '--port', dest='port', help='Specify the socket IO port')
    (options, args) = parser.parse_args()

    campr = Campr(port=options.port or 8001)

    def shutdown(sig, frame):
        campr.stop()
    signal.signal(signal.SIGABRT, shutdown)

    try:
        campr.start()
    except KeyboardInterrupt:
        campr.stop()
