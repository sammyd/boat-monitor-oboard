import random

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
        # Post data to the dispatcher
        self._dispatcher.post(data)




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

    def read_sample(self):
        data = dict()
        return data


class RandomDataSampleReader(SampleReader):
    '''
    This implementation generates a set number of random values
    '''

    def __init__(self, number_samples):
        self._number_samples = number_samples

    def read_sample(self):
        data = dict()
        for i in range(self._number_samples):
            data[i] = random.random()
        return data