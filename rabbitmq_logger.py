import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer

logger = logging.getLogger(__name__)
from colorama import init


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

init(autoreset=True)


async def cmd_handler(cmd):
    print(colorama.Fore.GREEN + f'{cmd}')


async def main():
    loop = asyncio.get_event_loop()
    consumer = Consumer('data', loop, cmd_handler)
    await consumer.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
