import logging
import time
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
        self.time = 0.0
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

    def gas_volume(self, pulses: int, diff_pulses: int) -> None:
        self.data_publisher.send_message(self.flowmeter.meter_id, str(pulses))
        logger.debug(colorama.Fore.GREEN + f'{self}: Measured volume {pulses}, diff: {diff_pulses}')
        logger.debug(colorama.Fore.GREEN + f'{self}: check volume {self.threshold}, diff: {self.difference_threshold}')
        if self.check_pulses(diff_pulses):
            self.flowmeter.stop()
            self.cmd_publisher.send_message(self.state_machine_id, str(self.threshold_cmd))

    def check_pulses(self, diff_pulses: int) -> bool:
        if diff_pulses != 0:
            self.time = time.time()
            return False

        return time.time() - self.time > 1.5

    def __repr__(self):
        return f'FlowmeterController {self.flowmeter.meter_id}'
