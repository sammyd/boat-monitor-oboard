import pika

class QueueWrapper:
    def post_message(self, message):
        raise NotImplementedError



class AQMPBlockingQueueManager(QueueWrapper):
    def post_message(self, message):
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.exchange_declare(exchange='raw_data', type='direct')
        channel.basic_publish(exchange='raw_data', routing_key=message[0], body=message[1])
        connection.close()



class AQMPAsyncQueueManager(QueueWrapper):
    def _on_open(self, connection):
        connection.channel(self._on_channel_open)

    def _on_channel_open(self, channel):
        channel.basic_publish('test_exchange',
                                'test_routing_key',
                                'message body value',
                                pika.BasicProperties(content_type='text/plain',
                                                     delivery_mode=1))
        self._connection.close()

    def post_message(self, message):
        # Step #1: Connect to RabbitMQ
        parameters = pika.URLParameters('localhost')
        self._connection = pika.SelectConnection(parameters=parameters,
                                           on_open_callback=self._on_open)

        try:
            # Step #2 - Block on the IOLoop
            self._connection.ioloop.start()
