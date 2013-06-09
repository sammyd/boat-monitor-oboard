'''
A dispatcher takes a queue object, formats the message appropriately and posts
it to the queue
'''

class Dispatcher:
    def __init__(self, queue_wrapper):
        self._queue_wrapper = queue_wrapper

    def post(self, data_object):
        '''
        data_object is a dictionary. We're going to post each entry in the
        dictionary as a different message to the queue. We'll use the key to
        specify which queue it should be dispatched to
        '''
        for key in data_object:
            # Post the message to the queue queue_wrapper
            self._queue_wrapper.post_message((key, data_object[key]))