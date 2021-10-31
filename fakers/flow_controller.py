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
        self.cmd_publisher = Publisher('data')
        self.flowmeter = FakeFlowMeter(config['name'], config['id'], config['flowrate'], self.gas_volume)
        self.trigger_cmd = config['trigger_command']
        self.threshold = config['threshold']['value']
        self.threshold_cmd = config['threshold']['command']
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
        if command == self.trigger_cmd:
            self.current_cmd = self.trigger_cmd
            self.flowmeter.measure()
            # if self.current_cmd == 'measure':
            #     self.flowmeter.measure()
            # elif self.current_cmd == 'stop':
            #     self.flowmeter.stop()

    def _command_for_node(self, cmd: dict):
        return cmd.get('messageType', '') == 'cmd' and cmd.get('node', '') == self.flowmeter.meter_id

    def gas_volume(self, volume: float) -> None:
        self.cmd_publisher.send_msg(self.flowmeter.meter_id, 'data', str(volume))
        logger.debug(colorama.Fore.GREEN + f'{self}: Measured volume {volume}')
        if volume > self.threshold:
            self.flowmeter.stop()
            self.cmd_publisher.send_msg(self.flowmeter.meter_id, 'data', str(self.threshold_cmd))

    def __repr__(self):
        return f'FakeFlowmeterController {self.flowmeter.meter_id}'
