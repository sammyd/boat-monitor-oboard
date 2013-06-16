from aglyph.binder import Binder

from onboard.input.data_reader import DataReader, SampleReader, RandomDataSampleReader, GPIODataSampleReader
from onboard.utils.dispatcher import Dispatcher
from onboard.utils.queue_wrapper import TxQueueWrapper, AQMPBlockingTxQueueManager
import pyev
from threading import Thread
from onboard.input.input_process import InputThread

class RawDataInputBinder(Binder):
    def __init__(self, configuration):
        super().__init__("raw-data-input-binder")
        self.bind(DataReader).init(SampleReader, Dispatcher, pyev.Loop, 2)
        self.bind(Dispatcher).init(TxQueueWrapper)
        self.bind(TxQueueWrapper, to=AQMPBlockingTxQueueManager, strategy="singleton").init(configuration['raw_data_exchange'])
        #self.bind(SampleReader, to=GPIODataSampleReader, strategy="singleton").init(configuration)
        self.bind(SampleReader, to=RandomDataSampleReader, strategy="singleton").init(configuration)
        self.bind(Thread, to=InputThread, strategy="singleton").init(pyev.Loop)
        self.bind(pyev.Loop, strategy="singleton")
