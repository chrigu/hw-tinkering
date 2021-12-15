import logging
import os

import asyncio

from web.fakers.motor_controller import FakeMotorController

logger = logging.getLogger(__name__)
from colorama import init


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

init(autoreset=True)

# motor cmd format: m<number>:on

# input date controller

# cmd + speed + position + done command, initial

RELEASE_MOTOR_CONFIG = {
    'name': 'Valve motor',
    'id': 'm2',
    'initial': 0,
    'speed': 10,
    'commands': {
        'open_release': {
            'speed': 2,
            'position': -90,
            'direction': -1,
            'done': 'release_open'
        },
        'close_release': {
            'speed': 2,
            'position': 0,
            'direction': 1,
            'done': 'release_closed'
        }
    }
}


async def main():
    loop = asyncio.get_event_loop()
    controller = FakeMotorController(loop, RELEASE_MOTOR_CONFIG)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
