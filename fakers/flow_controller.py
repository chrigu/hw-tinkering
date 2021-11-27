import logging
import colorama as colorama

from web.consumer import Consumer
from web.fakers.flowmeter import FakeFlowMeter

from web.publisher import Publisher

logger = logging.getLogger(__name__)


class FakeFlowMeterController:

    def __init__(self, loop, config: dict):
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.cmd_publisher = Publisher('cmd')
        self.data_publisher = Publisher('data')
        self.flowmeter = FakeFlowMeter(config['name'], config['id'], config['flowrate'], self.gas_volume)
        self.trigger_cmd = config['trigger_command']
        self.threshold = config['threshold']['value']
        self.threshold_cmd = config['threshold']['command']
        self.state_machine_id = config['state_machine_id']
        self.current_cmd = {}
        logger.debug(colorama.Fore.GREEN + f"{self}: Initialized")

    async def start_listen(self):
        await self.consumer.run()

    async def cmd_handler(self, cmd):
        logger.debug(colorama.Fore.GREEN + f"{self}: received {cmd}")
        if not self._command_for_node(cmd):
            logger.debug(colorama.Fore.YELLOW + f'{self}: Ignoring command')
            return

        command = cmd['data']

        logger.info(colorama.Fore.GREEN + f'{self}: {command}')
        if command == self.trigger_cmd:
            self.current_cmd = self.trigger_cmd
            self.flowmeter.measure()

    def _command_for_node(self, cmd: dict):
        return cmd.get('messageType', '') == 'cmd'

    def gas_volume(self, volume: float) -> None:
        print('some', volume)
        self.data_publisher.send_msg(self.flowmeter.meter_id, str(volume))
        logger.debug(colorama.Fore.GREEN + f'{self}: Measured volume {volume}')
        if volume > self.threshold:
            self.flowmeter.stop()
            self.cmd_publisher.send_msg(self.state_machine_id, str(self.threshold_cmd))

    def __repr__(self):
        return f'FakeFlowmeterController {self.flowmeter.meter_id}'
