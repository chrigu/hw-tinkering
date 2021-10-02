import json
import logging

import pika

LOGGER = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger('aio_pika').setLevel(logging.INFO)

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

    def send_msg(self, node: str, msg_type: str, data: str):
        LOGGER.info(f'Sending from {node} {msg_type}:{data}')
        self._channel.basic_publish('', self._queue_name,
                                    json.dumps({'messageType': msg_type, 'data': data, 'node': node}))
