from threading import Thread
from onboard.utils.queue_wrapper import RxQueueWrapperDelegate

class ConversionThread(Thread):
    def __init__(self, rx_queue_wrapper):
        super().__init__()
        self._rx_queue_wrapper = rx_queue_wrapper

    def run(self):
        self._rx_queue_wrapper.start()




class ConversionMessageProcessor(RxQueueWrapperDelegate):
    def __init__(self, dispatcher, conversionFactory):
        self._conversionFactory = conversionFactory
        self._dispatcher = dispatcher

    def message_received(self, message):
        '''
        Delegate method called when new message received. The message is a dictionary
        with the following keys:
         - timestamp
         - raw_value
         - type
         - sensor_id
        '''

        # Get hold of the right data convertor
        convertor = self._conversionFactory.create_value_convertor(message['type'])

        # Convert the value
        message['converted_value'] = convertor.convert(message['raw_value'])

        # Dispatch the message beyond
        self._dispatcher.post(message)

