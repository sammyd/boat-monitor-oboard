from aglyph.binder import Binder

from onboard.utils.queue_wrapper import RxQueueWrapper, RxQueueWrapperDelegate, LoggingRxQueueWrapperDelegate, AQMPRxQueueManager
from threading import Thread
from onboard.processing.conversion_process import ConversionThread

class ValueConversionBinder(Binder):
    def __init__(self):
        super().__init__("value-conversion-binder")
        self.bind(RxQueueWrapperDelegate, to=LoggingRxQueueWrapperDelegate, strategy="singleton")
        self.bind(RxQueueWrapper, to=AQMPRxQueueManager, strategy="singleton").init(RxQueueWrapperDelegate, "raw_data", "Queue0")
        self.bind(Thread, to=ConversionThread, strategy="singleton").init(RxQueueWrapper)
