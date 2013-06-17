import pika
import json
from pika.adapters.tornado_connection import TornadoConnection
import logging

class TxQueueWrapper:
    def post_message(self, message):
        raise NotImplementedError


class LoggingTxQueueManager(TxQueueWrapper):
    def post_message(self, message):
        print(message)


class AQMPBlockingTxQueueManager(TxQueueWrapper):
    def __init__(self, exchange):
        self._exchange = exchange

    def post_message(self, message):
        json_message = json.dumps(message[1])
        encoded_message = json_message.encode("UTF-8")
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange=self._exchange, type='direct')
        channel.basic_publish(exchange=self._exchange, routing_key=message[0], body=encoded_message)
        connection.close()


'''
Rx delegates
'''
class RxQueueWrapperDelegate:
    def message_received(self, message):
        raise NotImplementedError


class LoggingRxQueueWrapperDelegate:
    def message_received(self, message):
        print(message)



'''
2 Abstract Rx queue wrappers
'''
class RxQueueWrapper:
    def __init__(self, delegate):
        self._delegate = delegate

    def start(self):
        raise NotImplementedError


class RxMultiDelegateQueueWrapper:
    def __init__(self):
        self._delegates = set([])

    def start(self):
        raise NotImplementedError

    def add_delegate(self, delegate):
        self._delegates.add(delegate)

    def remove_delegate(self, delegate):
        try:
            self._delegates.remove(delegate)
        except KeyError:
            pass

    def notify_delegates(self, message):
        for delegate in self._delegates:
            delegate.message_received(message)


'''
And AQMP implementations
'''
class AQMPRxQueueManager(RxQueueWrapper):
    def __init__(self, delegate, exchange):
        super().__init__(delegate)

        self._exchange = exchange

        parameters = pika.ConnectionParameters(host='localhost')
        self._connection = pika.BlockingConnection(parameters = parameters)
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange=self._exchange, type='direct')


    def start(self, routing_key):
        # Get queue and bind to it
        result = self._channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self._channel.queue_bind(exchange=self._exchange, queue=queue_name, routing_key=routing_key)
        self._channel.basic_consume(self._callback, queue=queue_name, no_ack=True)

        # Start listening
        self._channel.start_consuming()

    def _callback(self, channel, method, properties, body):
        from_json = json.loads(body.decode("UTF-8"))
        self._delegate.message_received(from_json)



class AQMPMultiCastAsyncRxQueueManager(RxMultiDelegateQueueWrapper):
    def __init__(self, io_loop, exchange):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: __init__')
        self.io_loop = io_loop
        self.exchange = exchange
 
        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
 
    def start(self, routing_key):
        if self.connecting:
            self.logger.info('AQMPMultiCastAsyncRxQueueManager: Already connecting to RabbitMQ')
            return
 
        self.routing_key = routing_key
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: Connecting to RabbitMQ')
        self.connecting = True
 
        cred = pika.PlainCredentials('guest', 'guest')
        param = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host='/',
            credentials=cred
        )
 
        self.connection = TornadoConnection(param, on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)
        self.io_loop.start()
 
    # Callback 1
    def on_connected(self, connection):
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: connected to RabbitMQ')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)
 
    # Callback 2
    def on_channel_open(self, channel):
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: Channel open, Declaring exchange')
        self.channel = channel
        self.channel.queue_declare(exclusive=True, callback=self.on_queue_declared)

    # Callback 3
    def on_queue_declared(self, frame):
        """Called when RabbitMQ has told us our Queue has been declared, frame is the response from RabbitMQ"""
        self.queue_name = frame.method.queue
        self.channel.queue_bind(self.on_queue_bind, exchange=self.exchange, queue=self.queue_name, routing_key=self.routing_key)

    # Callback 4
    def on_queue_bind(self, frame):
        self.channel.basic_consume(self.on_message, queue=self.queue_name, no_ack=True)

    def on_closed(self, connection):
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: rabbit connection closed')
        self.io_loop.stop()
 
    def on_message(self, channel, method, header, body):
        self.logger.info('AQMPMultiCastAsyncRxQueueManager: message received: %s' % body)
        self.notify_delegates(body)
