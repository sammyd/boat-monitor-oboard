import logging
logger = logging.getLogger('onboard')
logger.setLevel(logging.WARN)

from onboard.input import RawDataInputBinder
from onboard.input.data_reader import DataReader
from threading import Thread
import time

from onboard.processing import ValueConversionBinder
from onboard.processing.conversion_process import ConversionProcess


from onboard.transmission import TransmissionBinder

config = {
    'input': [
        {
            'pin'  : 0,
            'type' : 'resistance',
            'id'   : 'pin0',
            'v_in' : 12.0,
            'r_ref': 4700
        },
        {
            'pin'  : 1,
            'type' : 'voltage',
            'id'   : 'pin1'
        },
        {
            'pin'  : 2,
            'type' : 'resistance',
            'id'   : 'pin2',
            'v_in' : 12.0,
            'r_ref': 47000
        }
    ],
    'raw_data_exchange' : 'raw_data',
    'input_accuracy' : 18,
    'processed' : {
        'data_exchange' : 'converted_data',
        'queue' : 'converted'
    }
}

'''
For demonstration purposes
'''
demo_config = {
    'input': [
        {
            'type' : 'random',
            'id'   : 'r1'
        },
        {
            'type' : 'random',
            'id'   : 'r2'
        }
    ],
    'raw_data_exchange' : 'raw_data',
    'input_accuracy' : 14,
    'processed' : {
        'data_exchange' : 'converted_data',
        'queue' : 'converted'
    }
}

#config = demo_config


input_binder = RawDataInputBinder(config)
input_thread = input_binder.lookup(Thread)
data_reader = input_binder.lookup(DataReader)

conversion_binder = ValueConversionBinder(config)
conversion_process = conversion_binder.lookup(ConversionProcess)

transmission_binder = TransmissionBinder(config)
transmission_thread = transmission_binder.lookup(Thread)


try:
  input_thread.start()
  conversion_process.start()
  transmission_thread.start()
  while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit):
  print ('\n! Received keyboard interrupt, quitting threads.\n')
