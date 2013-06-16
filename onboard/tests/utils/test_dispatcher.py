import unittest
from unittest.mock import Mock

from onboard.utils.dispatcher import Dispatcher

class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.mock_queue_wrapper = Mock()

    def test_DispatcherCallsQueueWrapperCorrectNumberOfTimes(self):
        data = dict({1: [12,12,12], 2: [24], 3: [7,13,12], 'hello': [26], "finally": []})
        dispatcher = Dispatcher(self.mock_queue_wrapper)
        dispatcher.post(data)
        total = 0
        for key in data:
            total += len(data[key])
        self.assertEqual(self.mock_queue_wrapper.post_message.call_count, total)