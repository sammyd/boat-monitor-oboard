import random
import time
from onboard.input.gpio_input import PiADCInput

class DataReader:
    '''
    Manages the data sampling. Attaches a sample reader to a provided event loop
    and then fires the data received onto a dispatcher
    '''

    def __init__(self, sample_reader, dispatcher, event_loop, sample_time):
        self._dispatcher = dispatcher
        self._event_loop = event_loop
        self._sample_reader = sample_reader
        self._start_sampling(sample_time)

    def _start_sampling(self, sample_time):
        # Add to the event loop
        self._timer = self._event_loop.timer(0, sample_time, self._timer_callback, 0)
        # And start the timer
        self._timer.start()

    def _timer_callback(self, watcher, revents):
        # Get the data
        data = self._sample_reader.read_sample()
        # Construct the correct data structure
        dict_to_send = dict()
        print(data)
        try:
            for dp in data:
                if 'type' in dp:
                    if dp['type'] not in dict_to_send:
                        dict_to_send[dp['type']] = list()
                    dict_to_send[dp['type']].append(dp)
        except TypeError:
            print("TypeError")

        # Post data to the dispatcher
        self._dispatcher.post(dict_to_send)



'''
Let's specify that the data points are dictionaries with the following keys:
 - timestamp
 - type
 - raw_value
 - sensor_id
'''


class SampleReader:
    '''
    Responsible for reading samples from different sources
    '''
    def read_sample(self):
        raise NotImplementedError()

class GPIODataSampleReader(SampleReader):
    '''
    This implementation will read samples from the GPIO for the Pi-ADC
    '''
    def __init__(self, configuration):
        self._config = configuration

    def _createADCSampler(self):
        # Need to prepare the config
        accuracy = self._config['input_accuracy']
        channels = []
        for input_config in self._config['input']:
            channels.append(input_config['pin'])
        self._piADCInput = PiADCInput(channels, accuracy)

    def read_sample(self):
        samples = self._piADCInput.getSamples()
        # Need to create data points of the correct form
        datapoints = list()
        for channel in samples:
            # Need to find the relevant line in the config
            cfg = self._input_config_for_channel(channel)
            # And now create the data point
            dp = dict()
            dp['timestamp'] = time.time()
            dp['raw_value'] = samples[channel]
            dp['sensor_id'] = cfg['id']
            dp['type']      = cfg['type']
            datapoints.append(dp)

        return datapoints

    def _input_config_for_channel(self, channel):
        pins = map(lambda x : x['pin'], self._config['input'])
        try:
            idx = list(pins).index(channel)
        except:
            print("problem")
        return self._config['input'][idx]


class RandomDataSampleReader(SampleReader):
    '''
    This implementation generates a set number of random values
    '''

    def __init__(self, configuration):
        self._config = configuration

    def read_sample(self):
        data = list()
        for sensor in self._config['input']:
            point = {
                      'timestamp': time.time(),
                           'type': 'random',
                      'raw_value': random.random(),
                      'sensor_id': sensor['id']
                    }
            data.append(point)
        return data

