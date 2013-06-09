from onboard.input import RawDataInputBinder
from onboard.input.data_reader import DataReader
from threading import Thread
import time


binder = RawDataInputBinder()
input_thread = binder.lookup(Thread)
data_reader = binder.lookup(DataReader)

try:
  input_thread.daemon=True
  input_thread.start()
  while True: time.sleep(100)
except (KeyboardInterrupt, SystemExit):
  print ('\n! Received keyboard interrupt, quitting threads.\n')
