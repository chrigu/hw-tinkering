import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer
from web.fakers.flowmeter import FakeFlowMeter

from web.publisher import Publisher

logger = logging.getLogger(__name__)
from colorama import init


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

init(autoreset=True)

# motor cmd format: m<number>:on

# input date controller


GAS_IN_FLOWMETER_CONFIG = {
    'name': 'Gas in flowmeter',
    'id': 'fm1',
    'flowrate': 30,
    'commands': {
        'open_gas': 'measure',
        'valve_closed': 'stop'
    }
}


class FakeFlowMeterController:

    def __init__(self, loop, config: dict):
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.cmd_publisher = Publisher('data')
        self.flowmeter = FakeFlowMeter(config['name'], config['id'], config['flowrate'], self.gas_volume)
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

        command = cmd['data']

        logger.info(colorama.Fore.GREEN + f'{self}: {command}')
        if command in [*self.commands]:
            self.current_cmd = self.commands[command]
            if self.current_cmd == 'measure':
                self.flowmeter.measure()
            elif self.current_cmd == 'stop':
                self.flowmeter.stop()

    def _command_for_node(self, cmd: dict):
        return cmd.get('messageType', '') == 'cmd' and cmd.get('node', '') == self.flowmeter.meter_id

    def gas_volume(self, volume: float) -> None:
        self.cmd_publisher.send_msg(self.flowmeter.meter_id, 'data', str(volume))
        logger.debug(colorama.Fore.GREEN + f'{self}: Measured volume {volume}')
        if volume > 90:
            self.flowmeter.stop()

    def __repr__(self):
        return f'FakeFlowmeterController {self.flowmeter.meter_id}'


async def main():
    loop = asyncio.get_event_loop()
    controller = FakeFlowMeterController(loop, GAS_IN_FLOWMETER_CONFIG)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
