from threading import Thread

class ConversionThread(Thread):
    def __init__(self, rx_queue_wrapper):
        super().__init__()
        self._rx_queue_wrapper = rx_queue_wrapper

    def run(self):
        self._rx_queue_wrapper.start()