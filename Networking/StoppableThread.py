import threading

class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args):
        self._stopEvent = threading.Event()
        super().__init__(*args)
        

    def stop(self):
        self._stopEvent.set()

    def stopped(self):
        return self._stopEvent.isSet()
