import asyncio
import json

import aio_pika


class Consumer(object):

    _connection = None

    def __init__(self, exchange_name, loop, message_handler):

        self._loop = loop
        self._exchange_name = exchange_name
        self._message_handler = message_handler

    async def run(self):
        self._connection = await aio_pika.connect_robust(
            "amqp://guest:guest@localhost:5672/"
        )

        channel = await self._connection.channel()
        exchange = await channel.declare_exchange(self._exchange_name, type='fanout')

        # Declaring queue
        queue = await channel.declare_queue('', exclusive=True)
        await queue.bind(exchange, '')
        await queue.consume(self._process_message, no_ack=False)

        return self._connection

    async def _process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body_as_string = "".join(chr(x) for x in message.body)
            msg_data = json.loads(body_as_string)
            await self._message_handler(msg_data)


