import logging
import os

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


class FakeMotorController:

    def __init__(self, loop, config: dict):
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.data_publisher = Publisher('data')
        self.cmd_publisher = Publisher('cmd')
        self.motor = FakeMotor(config['initial'], config['speed'], config['name'], config['id'], self.motor_position)
        self.commands = config['commands']
        self.current_cmd = {}
        logger.debug(colorama.Fore.GREEN + f"{self}: Initialized")
        # asyncio.ensure_future(consumer.run())

    async def start_listen(self):
        await self.consumer.run()

    async def cmd_handler(self, cmd):
        logger.debug(colorama.Fore.GREEN + f"{self}: received {cmd}")
        if not self._command_for_node(cmd):
            logger.debug(colorama.Fore.YELLOW + f'{self}: Ignoring command')
            return

        command_name = cmd.get('data', '')

        logger.info(colorama.Fore.GREEN + f'{self}: {command_name}')

        if command_name in [*self.commands]:
            self.current_cmd = self.commands[command_name]
            self.motor.turn(self.current_cmd['position'], self.current_cmd['direction'])

    def _command_for_node(self, cmd: dict):
        return cmd.get('messageType', '') == 'cmd'

    def motor_position(self, position: float, done: bool) -> None:
        self.data_publisher.send_msg(self.motor.motor_id, str(position))
        logger.debug(colorama.Fore.GREEN + f'{self}: Motor at position {position}')
        if done:
            logger.debug(colorama.Fore.GREEN + f'{self}: Motor done')
            self.cmd_publisher.send_msg(self.motor.motor_id, self.current_cmd['done'])

    def __repr__(self):
        return f'FakeMotorController {self.motor.motor_id}'
