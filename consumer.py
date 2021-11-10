import json

import aio_pika


class Consumer(object):

    _connection = None

    def __init__(self, queue_name, loop, message_handler):

        self._loop = loop
        self._queue_name = queue_name
        self._message_handler = message_handler

    async def run(self):
        self._connection = await aio_pika.connect_robust(
            "amqp://guest:guest@localhost:5672/%2F"
        )

        channel = await self._connection.channel()

        # Maximum message count which will be
        # processing at the same time.
        await channel.set_qos(prefetch_count=1)

        # Declaring queue
        queue = await channel.declare_queue(self._queue_name, auto_delete=False)

        await queue.consume(self._process_message)

        return self._connection

    async def _process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body_as_string = "".join(chr(x) for x in message.body)
            msg_data = json.loads(body_as_string)
            await self._message_handler(msg_data)
