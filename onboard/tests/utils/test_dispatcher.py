import unittest
from unittest.mock import Mock

from onboard.utils.dispatcher import Dispatcher

class TestDispatcher(unittest.TestCase):
    def setUp(self):
        self.mock_queue_wrapper = Mock()

    def test_DispatcherCallsQueueWrapperCorrectNumberOfTimes(self):
        data = dict({1: 12, 2: 24, 3: 7, 'hello': 26, "finally": 27})
        dispatcher = Dispatcher(self.mock_queue_wrapper)
        dispatcher.post(data)
        self.assertEqual(self.mock_queue_wrapper.post_message.call_count, len(data))