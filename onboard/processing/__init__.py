from aglyph.binder import Binder

from onboard.utils.queue_wrapper import RxQueueWrapper, RxQueueWrapperDelegate, LoggingRxQueueWrapperDelegate, AQMPRxQueueManager
from onboard.processing.conversion_process import ConversionThread, ConversionProcess, ConversionMessageProcessor
from onboard.utils.dispatcher import Dispatcher
from onboard.utils.queue_wrapper import LoggingTxQueueManager, TxQueueWrapper
from onboard.processing.value_convertor_factory import ValueConvertorFactory, OnboardValueConvertorFactory

class ValueConversionBinder(Binder):
    def __init__(self, configuration):
        super().__init__("value-conversion-binder")

        # Input from the queue
        self.bind(RxQueueWrapper, to=AQMPRxQueueManager, strategy="prototype").init(RxQueueWrapperDelegate, configuration['raw_data_exchange'])

        # Processing
        #self.bind(RxQueueWrapperDelegate, to=LoggingRxQueueWrapperDelegate, strategy="prototype")
        self.bind(RxQueueWrapperDelegate, to=ConversionMessageProcessor, strategy="prototype").init(Dispatcher, ValueConvertorFactory, configuration)
        self.bind(ValueConvertorFactory, to=OnboardValueConvertorFactory)

        # And transmission of the converted values
        self.bind(Dispatcher).init(TxQueueWrapper)
        self.bind(TxQueueWrapper, to=LoggingTxQueueManager)
        
        # Thread and process management
        self.bind(ConversionThread, strategy="prototype").init(RxQueueWrapper)
        self.bind(ConversionProcess, strategy="singleton").init(configuration, self)
