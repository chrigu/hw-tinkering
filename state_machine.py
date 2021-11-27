import logging
import os
import colorama as colorama

import asyncio
from enum import Enum
from transitions import Machine

from web.consumer import Consumer
from web.publisher import Publisher

logger = logging.getLogger(__name__)

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

colorama.init(autoreset=True)


class BlowoffState(Enum):
    OFF = False
    ON = True


MOTOR_CONFIG = {
    'main_valve': 'm1',
    'blowoff': 'm2',
    'gas_input': 'fm1',
    'gas_output': 'fm2'
}


class FillState(Enum):
    OFF = 0
    OPENING_GAS = 1
    GAS_OPEN = 2
    CLOSING_GAS = 3
    OPENING_LIQUID = 4
    LIQUID_OPEN = 5
    OPENING_RELEASE = 6
    FILLING = 7
    CLOSING_RELEASE = 8
    RELEASE_CLOSED = 9
    CLOSING_LIQUID = 10
    TRI_NEUTRAL = 11


class BottleFiller:

    states = [
        {'name': 'off', 'on_enter': ['shutoff']},
        {'name': 'opening gas', 'on_enter': ['open_gas']},
        'gas open',
        {'name': 'closing gas', 'on_enter': ['close_gas']},
        {'name': 'opening liquid', 'on_enter': ['open_liquid']},
        {'name': 'liquid open', 'on_enter': ['open_release']},
        'filling liquid',
        {'name': 'closing release', 'on_enter': ['close_release']},
        {'name': 'closing liquid', 'on_enter': ['close_liquid']},
        'tri neutral',
    ]

    transitions = [
        {'trigger': 'start', 'source': 'off', 'dest': 'opening gas'},
        {'trigger': 'gas_open', 'source': 'opening gas', 'dest': 'gas open'},
        {'trigger': 'gas_filled', 'source': 'gas open', 'dest': 'closing gas'},
        {'trigger': 'gas_closed', 'source': 'closing gas', 'dest': 'opening liquid'},
        {'trigger': 'liquid_open', 'source': 'opening liquid', 'dest': 'liquid open'},
        {'trigger': 'release_open', 'source': 'liquid open', 'dest': 'filling liquid'},
        {'trigger': 'filled', 'source': ['filling liquid', 'liquid open'], 'dest': 'closing release'},
        {'trigger': 'release_closed', 'source': 'closing release', 'dest': 'closing liquid'},
        {'trigger': 'liquid_closed', 'source': 'closing liquid', 'dest': 'off'},
        {'trigger': 'abort', 'source': '*', 'dest': 'off'},
    ]

    def __init__(self, loop, id):
        self.id = id
        self.machine = Machine(model=self, states=BottleFiller.states, transitions=BottleFiller.transitions,
                               initial='off')
        self.cmd_publisher = Publisher('cmd')
        self.cmd_consumer = Consumer('cmd', loop, self.consumer_handler)
        self.data_consumer = Consumer('data', loop, self.consumer_handler)

    async def start_listen(self):
        await self.cmd_consumer.run()
        await self.data_consumer.run()

    async def consumer_handler(self, data: dict):
        logger.debug(colorama.Fore.GREEN + f'{self} data: {data}')
        if data['node'] != self.id:
            return
        if self.is_data(data):
            self.data_handler(data)
        else:
            self.cmd_handler(data)

    def data_handler(self, data: dict):
        logger.debug(colorama.Fore.YELLOW + f'{self} data_handler: {data}')

    def cmd_handler(self, data: dict):
        logger.debug(colorama.Fore.YELLOW + f'{self} cmd_handler: {data}')
        valid_triggers = map(lambda x: x['trigger'], self.transitions)

        if data['data'] not in valid_triggers:
            logger.debug(colorama.Fore.RED + f'{self} cmd_handler: No valid trigger {data["data"]}')
            return

        self.call_trigger(data['data'])

    def call_trigger(self, data):
        getattr(self, data)()

    def is_data(self, data: dict) -> bool:
        return data.get('messageType', '') == 'data'

    def open_gas(self):
        self._send_cmd('open_gas')

    def close_gas(self):
        self._send_cmd('close_gas')

    def open_liquid(self):
        self._send_cmd('open_liquid')

    def open_release(self):
        self._send_cmd('open_release')

    def close_release(self):
        self._send_cmd('close_release')

    def close_liquid(self):
        self._send_cmd('close_liquid')

    def close_liquid(self):
        self._send_cmd('close_liquid')

    def shutoff(self):
        self._send_cmd('shutoff')

    def _send_cmd(self, cmd):
        logger.debug(colorama.Fore.GREEN + f"{self}: Sending '{cmd}')")
        self.cmd_publisher.send_msg('sm', cmd)

    def __repr__(self):
        return f'BottleFiller'


async def main():
    loop = asyncio.get_event_loop()
    filler = BottleFiller(loop, 'sm')
    await filler.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
