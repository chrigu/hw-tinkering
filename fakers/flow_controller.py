import logging
import os

import colorama as colorama

from web.consumer import Consumer
from web.fakers.flowmeter import FakeFlowMeter

from web.publisher import Publisher

logger = logging.getLogger(__name__)

LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)


class FlowMeterController:

    def __init__(self, config: dict, cmd_publisher: Publisher, data_publisher: Publisher, consumer: Consumer,
                 flowmeter: FakeFlowMeter):
        self.consumer = consumer
        self.cmd_publisher = cmd_publisher
        self.data_publisher = data_publisher
        self.flowmeter = flowmeter

        self.consumer.set_message_handler(self.cmd_handler)
        self.flowmeter.set_flow_cb(self.gas_volume)

        self.trigger_cmd = config.get('trigger_command', '')
        self.threshold = config['threshold']['value']
        self.threshold_cmd = config['threshold']['command']
        self.state_machine_id = config['state_machine_id']
        self.difference_threshold = config['threshold'].get('difference', 1000)
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

    def gas_volume(self, volume: float, diff_volume: float) -> None:
        self.data_publisher.send_message(self.flowmeter.meter_id, str(volume))
        logger.debug(colorama.Fore.GREEN + f'{self}: Measured volume {volume}, diff: {diff_volume}')
        if self.check_volume(volume, diff_volume):
            self.flowmeter.stop()
            self.cmd_publisher.send_message(self.state_machine_id, str(self.threshold_cmd))

    def check_volume(self, volume: float, diff_volume: float):
            return volume > self.threshold and diff_volume < self.difference_threshold

    def __repr__(self):
        return f'FlowmeterController {self.flowmeter.meter_id}'
