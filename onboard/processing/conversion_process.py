from threading import Thread
from onboard.utils.queue_wrapper import RxQueueWrapperDelegate

class ConversionThread(Thread):
    def __init__(self, rx_queue_wrapper):
        super().__init__()
        self.rx_queue_wrapper = rx_queue_wrapper
        self.daemon = True

    def run(self):
        self.rx_queue_wrapper.start(self.routing_key)




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


class ConversionProcess:
    def __init__(self, configuration, binder):
        self._config = configuration
        self.conversionBinder = binder
        self.createThreads()

    def createThreads(self):
        # We want one thread per queue. We work that out from the config
        queues = []
        try:
            for input_type in self._config['input']:
                if input_type['type'] not in queues:
                    queues.append(input_type['type'])
        except:
            print("Problem generating queue list")

        # Now create the threads
        self._threads = []
        for queue_type in queues:
            new_thread = self.conversionBinder.lookup(ConversionThread)
            new_thread.routing_key = queue_type
            self._threads.append(new_thread)



    def start(self):
        for thread in self._threads:
            thread.start()