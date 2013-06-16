from threading import Thread

class InputThread(Thread):
    def __init__(self, event_loop):
        super().__init__()
        self.daemon = True
        self._event_loop = event_loop

    def run(self):
        print("Starting event loop")
        self._event_loop.start()

    def abort(self):
        self._event_loop.stop()