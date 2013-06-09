from aglyph.binder import Binder

from onboard.input.data_reader import DataReader, SampleReader, RandomDataSampleReader
from onboard.utils.dispatcher import Dispatcher
from onboard.utils.queue_wrapper import TxQueueWrapper, AQMPBlockingTxQueueManager
import pyev
from threading import Thread
from onboard.input.input_process import InputThread

class RawDataInputBinder(Binder):
    def __init__(self):
        super().__init__("raw-data-input-binder")
        self.bind(DataReader).init(SampleReader, Dispatcher, pyev.Loop, 2)
        self.bind(Dispatcher).init(TxQueueWrapper)
        self.bind(TxQueueWrapper, to=AQMPBlockingTxQueueManager, strategy="singleton").init("raw_data")
        self.bind(SampleReader, to=RandomDataSampleReader, strategy="singleton").init(2)
        self.bind(Thread, to=InputThread, strategy="singleton").init(pyev.Loop)
        self.bind(pyev.Loop, strategy="singleton")
