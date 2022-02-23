import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer
from web.fakers.flow_controller import FlowMeterController
from web.fakers.flowmeter import FakeFlowMeter
from web.publisher import MqttPublisher

logger = logging.getLogger(__name__)
from colorama import init


LOGLEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()
logger.setLevel(LOGLEVEL)

init(autoreset=True)

# motor cmd format: m<number>:on

# input date controller


GAS_IN_FLOWMETER_CONFIG = {
    'name': 'Gas out flowmeter',
    'id': 'fm2',
    'flowrate': 10,  # only for fake
    'trigger_command': 'open_release',
    'state_machine_id': 'sm',
    'threshold': {
        'value': 100,
        'command': 'filled'
    }
}


async def main():
    loop = asyncio.get_event_loop()
    consumer = Consumer('cmd', loop)
    cmd_publisher = MqttPublisher('cmd')
    data_publisher = MqttPublisher('data')
    flowmeter = FakeFlowMeter(GAS_IN_FLOWMETER_CONFIG['name'], GAS_IN_FLOWMETER_CONFIG['id'],
                              GAS_IN_FLOWMETER_CONFIG['flowrate'])
    controller = FlowMeterController(GAS_IN_FLOWMETER_CONFIG, cmd_publisher, data_publisher, consumer, flowmeter)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
