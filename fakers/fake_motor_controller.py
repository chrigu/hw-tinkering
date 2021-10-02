import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer

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


class FakeMotorController:

    def __init__(self, loop, config: dict):
        logger.debug(colorama.Fore.GREEN + f"Initializing fake controller for {config['id']}")
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.cmd_publisher = Publisher('data')
        self.motor = FakeMotor(config['initial'], config['speed'], config['name'], config['id'], self.motor_position)
        self.commands = config['commands']
        self.current_cmd = {}
        # asyncio.ensure_future(consumer.run())

    async def start_listen(self):
        await self.consumer.run()

    async def cmd_handler(self, cmd):
        logger.debug(colorama.Fore.GREEN + f"Fake controller for {self.motor.motor_id} received {cmd}")
        if not self._command_for_node(cmd):
            logger.debug(f'Ignoring command for {self.motor.motor_id}. Got {cmd}')
            return

        command = cmd['data']

        # logger.info(colorama.Fore.YELLOW + f'{self.motor.motor_id} FakeController got: {command}')
        print(colorama.Fore.YELLOW + f'{self.motor.motor_id} FakeController got: {command}')
        if command in [*self.commands]:
            self.current_cmd = self.commands[command]
            self.motor.turn(self.current_cmd['position'], self.current_cmd['direction'])

    def _command_for_node(self, cmd: dict):
        return cmd.get('messageType', '') == 'cmd' and cmd.get('node', '') == self.motor.motor_id

    def motor_position(self, position: float, done: bool) -> None:
        self.cmd_publisher.send_msg(self.motor.motor_id, 'data', str(position))
        print(f'Fakemotor {self.motor.motor_id} at position {position}')
        if done:
            self.cmd_publisher.send_msg(self.motor.motor_id, 'data', self.current_cmd['done'])


async def main():
    loop = asyncio.get_event_loop()
    controller = FakeMotorController(loop, VALVE_MOTOR_CONFIG)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
