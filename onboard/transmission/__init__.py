from aglyph.binder import Binder

from onboard.utils.queue_wrapper import RxMultiDelegateQueueWrapper, AQMPMultiCastAsyncRxQueueManager
from threading import Thread
from onboard.transmission.transmission_process import TransmissionThread

from tornado import ioloop



class TransmissionBinder(Binder):
    def __init__(self, configuration):
        super().__init__("transmission-binder")

        # Input from the queue
        self.bind(RxMultiDelegateQueueWrapper, to=AQMPMultiCastAsyncRxQueueManager, strategy="singleton").init(ioloop.IOLoop.instance(), configuration['processed']['data_exchange'])

        # And the thread
        self.bind(Thread, to=TransmissionThread, strategy="singleton").init(RxMultiDelegateQueueWrapper, configuration['processed']['queue'])