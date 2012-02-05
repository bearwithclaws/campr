#! /usr/bin/env python
"""
The server that starts (and stops) the Campr app.
"""
import signal
from campr import Campr

if __name__ == "__main__":
    campr = Campr()

    def shutdown(sig, frame):
        campr.stop()
    signal.signal(signal.SIGABRT, shutdown)

    try:
        campr.start()
    except KeyboardInterrupt:
        campr.stop()
