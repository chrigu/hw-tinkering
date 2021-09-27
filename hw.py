import logging
import asyncio

# from adafruit_servokit import ServoKit

from consumer import Consumer
from valve import Valve

# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
from publisher import Publisher
from web.state_machine import ValveState, Events, FillState

logger = logging.getLogger(__name__)


class HwController:

    def __init__(self, loop):
        # self.kit = ServoKit(channels=16)
        # self.kit.servo[0].angle = 0
        # use the same loop to consume
        # asyncio.ensure_future(consume(loop))
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.cmd_publisher = Publisher('data')
        self.valve = Valve()
        self.valve.neutral()
        self.valve_state = ValveState.NEUTRAL
        # asyncio.ensure_future(consumer.run())

    async def start_listen(self):
        await self.consumer.run()

    async def cmd_handler(self, cmd):
        logger.debug(f'Got cmd: {cmd}')
        if cmd['cmd'] == Events.START and self.valve_state == ValveState.NEUTRAL:
            for a in range(0, 60):
                print(a)
                await self.loop.run_in_executor(None, self.cmd_publisher.send_msg, {'data': a})

                await asyncio.sleep(0.1)
                # self.kit.servo[0].angle = 180



async def main():
    loop = asyncio.get_event_loop()
    hw = HwController(loop)
    await hw.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
