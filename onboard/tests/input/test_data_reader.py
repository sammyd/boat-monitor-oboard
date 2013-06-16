import unittest
from unittest.mock import Mock

from onboard.input.data_reader import RandomDataSampleReader
from onboard.input.data_reader import DataReader

class TestDataReader(unittest.TestCase):

    def setUp(self):
        self.mock_event_loop = Mock()
        self.mock_dispatcher = Mock()
        self.mock_sample_reader = Mock()
        self.sample_time = 5
        self.data_reader = DataReader(self.mock_sample_reader, self.mock_dispatcher, self.mock_event_loop, self.sample_time)

    def test_StartSamplingAddsToEventLoop(self):
        self.mock_event_loop.timer.assert_called_once_with(0, self.sample_time, self.data_reader._timer_callback, 0)

    def test_TimerCallBackAttemptsToDispatch(self):
        d = [{'type': 'first', 'value': 1}, {'type': 'first', 'value': 2}, {'type': 'second', 'value': 3}]
        self.mock_sample_reader.read_sample.return_value = d
        self.data_reader._timer_callback(None, None)
        expected_return = { 'first': [d[0], d[1]], 'second': [d[2]]}
        self.mock_dispatcher.post.assert_called_once_with(expected_return)

    def test_TimerCallBackAttemptsToCollectSampleData(self):
        self.data_reader._timer_callback(None, None)
        self.mock_sample_reader.read_sample.assert_called()


class TestRandomDataSampleReader(unittest.TestCase):

    def test_ReturnsDictionaryOfCorrectSize(self):
        cfg = { 'input' : [] }
        for i in range(10):
            cfg['input'].append({'type': 'random', 'id': i })
        sample_reader = RandomDataSampleReader(cfg)
        data = sample_reader.read_sample()
        self.assertTrue(len(data) == len(cfg['input']))

