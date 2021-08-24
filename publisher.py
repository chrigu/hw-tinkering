import json
import logging

import pika

LOGGER = logging.getLogger(__name__)

class Publisher:

    def __init__(self, queue_name):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1',
                                               5672,
                                               '/',
                                               credentials)

        self._queue_name = queue_name
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

        self._channel.queue_declare(queue=self._queue_name)

    def send_msg(self, message):
        LOGGER.info(f'Sending to {message}')
        self._channel.basic_publish('', self._queue_name, json.dumps({'cmd': message}))
