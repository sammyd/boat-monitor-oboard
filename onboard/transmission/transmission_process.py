from threading import Thread

class TransmissionThread(Thread):
    def __init__(self, rx_queue_wrapper, queue):
        super().__init__()
        self.rx_queue_wrapper = rx_queue_wrapper
        self.daemon = True
        self.routing_key = queue

    def run(self):
        self.rx_queue_wrapper.start(self.routing_key)