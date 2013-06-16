from aglyph.binder import Binder

from onboard.utils.queue_wrapper import RxQueueWrapper, RxQueueWrapperDelegate, LoggingRxQueueWrapperDelegate, AQMPRxQueueManager
from onboard.processing.conversion_process import ConversionThread, ConversionProcess

class ValueConversionBinder(Binder):
    def __init__(self, configuration):
        super().__init__("value-conversion-binder")
        self.bind(RxQueueWrapperDelegate, to=LoggingRxQueueWrapperDelegate, strategy="prototype")
        self.bind(RxQueueWrapper, to=AQMPRxQueueManager, strategy="prototype").init(RxQueueWrapperDelegate, configuration['raw_data_exchange'])
        self.bind(ConversionThread, strategy="prototype").init(RxQueueWrapper)
        self.bind(ConversionProcess, strategy="singleton").init(configuration, self)
