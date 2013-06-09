from onboard.input import RawDataInputBinder
from onboard.input.data_reader import DataReader
from threading import Thread
import time

from onboard.processing import ValueConversionBinder

input_binder = RawDataInputBinder()
input_thread = input_binder.lookup(Thread)
data_reader = input_binder.lookup(DataReader)

conversion_binder = ValueConversionBinder()
conversion_thread = conversion_binder.lookup(Thread)

try:
  input_thread.daemon=True
  input_thread.start()
  conversion_thread.daemon=True
  conversion_thread.start()
  while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit):
  print ('\n! Received keyboard interrupt, quitting threads.\n')
