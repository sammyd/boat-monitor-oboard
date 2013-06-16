import pika
import json

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




class RxQueueWrapperDelegate:
    def message_received(self, message):
        raise NotImplementedError


class LoggingRxQueueWrapperDelegate:
    def message_received(self, message):
        print(message)



class RxQueueWrapper:
    def __init__(self, delegate):
        self._delegate = delegate

    def start(self):
        raise NotImplementedError

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



