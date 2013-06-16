from aglyph.binder import Binder

from onboard.utils.queue_wrapper import RxQueueWrapper, RxQueueWrapperDelegate, AQMPRxQueueManager, LoggingRxQueueWrapperDelegate
from threading import Thread
from onboard.transmission.transmission_process import TransmissionThread



class TransmissionBinder(Binder):
    def __init__(self, configuration):
        super().__init__("transmission-binder")

        # Input from the queue
        self.bind(RxQueueWrapper, to=AQMPRxQueueManager, strategy="prototype").init(RxQueueWrapperDelegate, configuration['processed']['data_exchange'])

        # Log the output
        self.bind(RxQueueWrapperDelegate, to=LoggingRxQueueWrapperDelegate, strategy="prototype")

        # And the thread
        self.bind(Thread, to=TransmissionThread, strategy="singleton").init(RxQueueWrapper, configuration['processed']['queue'])