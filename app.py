from onboard.input import RawDataInputBinder
from onboard.input.data_reader import DataReader
from threading import Thread
import time

from onboard.processing import ValueConversionBinder
from onboard.processing.conversion_process import ConversionProcess

import logging

logger = logging.getLogger('onboard')
logger.setLevel(logging.DEBUG)

from onboard.transmission import TransmissionBinder

config = {
    'input': [
        {
            'pin'  : 0,
            'type' : 'resistance',
            'id'   : 'pin0',
            'v_in' : 12.0,
            'r_ref': 10000
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
    'input_accuracy' : 14,
    'processed' : {
        'data_exchange' : 'converted_data',
        'queue' : 'converted'
    }
}

'''
For demonstration purposes
'''
config = {
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


input_binder = RawDataInputBinder(config)
input_thread = input_binder.lookup(Thread)
data_reader = input_binder.lookup(DataReader)

conversion_binder = ValueConversionBinder(config)
conversion_process = conversion_binder.lookup(ConversionProcess)

#transmission_binder = TransmissionBinder(config)
#transmission_thread = transmission_binder.lookup(Thread)


import tornado, pika
from tornado import websocket
from onboard.utils.queue_wrapper import AQMPMultiCastAsyncRxQueueManager

class MyWebSocketHandler(websocket.WebSocketHandler):
 
    def open(self, *args, **kwargs):
        self.application.pc.add_event_listener(self)
        #pika.log.info("WebSocket opened")
 
    def on_close(self):
        #pika.log.info("WebSocket closed")
        self.application.pc.remove_event_listener(self)

application = tornado.web.Application([
    (r'/ws', MyWebSocketHandler),
])
#pika.log.setup(color=True) 
io_loop = tornado.ioloop.IOLoop.instance()

# PikaClient is our rabbitmq consumer
pc = AQMPMultiCastAsyncRxQueueManager(io_loop, 'converted_data')
application.pc = pc
application.pc.connect('converted')

application.listen(8888)


try:
  input_thread.start()
  conversion_process.start()
  #transmission_thread.start()
  io_loop.start()
  while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit):
  print ('\n! Received keyboard interrupt, quitting threads.\n')
