import logging
import os

import asyncio
import colorama as colorama

from web.consumer import RabbitConsumer
from web.fakers.flow_controller import FlowMeterController
from web.fakers.flowmeter import FakeFlowMeter
from web.publisher import RabbitPublisher

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
    'flow_rates': [
        {
            "duration": 4,
            "pulses": 29
        },
        {
            "duration": 1.6,
            "pulses": 0
        },
    ],
    'trigger_command': 'open_release',
    'state_machine_id': 'sm',
    'threshold': {
        'value': 100,
        'command': 'filled',
        'threshold': 100
    }
}


async def main():
    loop = asyncio.get_event_loop()
    consumer = RabbitConsumer('cmd', loop)
    cmd_publisher = RabbitPublisher('cmd')
    data_publisher = RabbitPublisher('data')
    flowmeter = FakeFlowMeter(GAS_IN_FLOWMETER_CONFIG['name'], GAS_IN_FLOWMETER_CONFIG['id'],
                              GAS_IN_FLOWMETER_CONFIG['flow_rates'])
    controller = FlowMeterController(GAS_IN_FLOWMETER_CONFIG, cmd_publisher, data_publisher, consumer, flowmeter)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
