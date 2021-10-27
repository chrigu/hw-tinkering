import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer
from web.fakers.fake_motor_controller import FakeMotorController

from web.publisher import Publisher
from web.fakers.motor import FakeMotor

logger = logging.getLogger(__name__)
from colorama import init


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

init(autoreset=True)

# motor cmd format: m<number>:on

# input date controller

# cmd + speed + position + done command, initial

VALVE_MOTOR_CONFIG = {
    'name': 'Valve motor',
    'id': 'm1',
    'initial': 0,
    'speed': 30,
    'commands': {
        'open_gas': {
            'speed': 30,
            'position': -90,
            'direction': -1,
            'done': 'gas_open'
        }
    }
}

async def main():
    loop = asyncio.get_event_loop()
    controller = FakeMotorController(loop, VALVE_MOTOR_CONFIG)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
