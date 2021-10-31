import logging
import os

import asyncio
import colorama as colorama

from web.consumer import Consumer
from web.fakers.flow_controller import FakeFlowMeterController
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
    'flowrate': 30, #only for faek
    'trigger': 'open_gas',
    'threshold': {
        'value': 100,
        'command': 'close_valve'
    }
}


async def main():
    loop = asyncio.get_event_loop()
    controller = FakeFlowMeterController(loop, GAS_IN_FLOWMETER_CONFIG)
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
