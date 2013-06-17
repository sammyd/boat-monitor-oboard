from threading import Thread
import logging
from tornado import websocket
import tornado
from onboard.utils.queue_wrapper import RxQueueWrapperDelegate

class TransmissionThread(Thread):
    def __init__(self, rx_queue_wrapper, queue):
        super().__init__()
        self.rx_queue_wrapper = rx_queue_wrapper
        self.daemon = True
        self.routing_key = queue

        self.websocket_worker = tornado.web.Application([
            (r'/ws', OnboardWebSocketTransmissionHandler, { "rx_queue" : rx_queue_wrapper } ),
        ])
        self.websocket_worker.listen(8888)

    def run(self):
        self.rx_queue_wrapper.start(self.routing_key)



class RxQueueDelegateWebsocketWrapper(RxQueueWrapperDelegate):
    def __init__(self, websocket):
        self._websocket = websocket

    def message_received(self, message):
        self._websocket.write_message(message)


class OnboardWebSocketTransmissionHandler(websocket.WebSocketHandler):
    def __init__(self, application, request, rx_queue=None, **kwargs):
        super().__init__(application, request, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.rx_queue = rx_queue

    def open(self, *args, **kwargs):
        self.delegate_wrapper = RxQueueDelegateWebsocketWrapper(self)
        self.rx_queue.add_delegate(self.delegate_wrapper)
        self.logger.info("WebSocket opened")
 
    def on_close(self):
        self.logger.info("WebSocket closed")
        self.rx_queue.remove_delegate(self.delegate_wrapper)

