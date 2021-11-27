import json
import logging

import pika

LOGGER = logging.getLogger(__name__)

logging.basicConfig()
logging.getLogger('aio_pika').setLevel(logging.INFO)


class Publisher:

    def __init__(self, data_type):
        credentials = pika.PlainCredentials('guest', 'guest')
        parameters = pika.ConnectionParameters('127.0.0.1',
                                               5672,
                                               '/',
                                               credentials)

        self._data_type = data_type
        self._connection = pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()

        self._channel.exchange_declare(exchange=data_type, exchange_type='fanout')

    def send_msg(self, node: str, data: str):
        LOGGER.info(f'Sending from {node} {self._data_type}:{data}')
        self._channel.basic_publish(exchange=self._data_type, routing_key='',
                                    body=bytes(json.dumps({'messageType': self._data_type,
                                                           'data': data, 'node': node}), 'utf-8'))
