import logging
import asyncio
import colorama as colorama

from web.consumer import Consumer
from web.fakers.main_valve import FakeMainValve

from web.publisher import Publisher

logger = logging.getLogger(__name__)
from colorama import init


init(autoreset=True)

# motor cmd format: m<number>:on


class FakeValveController:

    def __init__(self, loop, valve_id, valve_name):
        # self.kit = ServoKit(channels=16)
        # self.kit.servo[0].angle = 0
        # use the same loop to consume
        # asyncio.ensure_future(consume(loop))
        self.loop = loop
        self.consumer = Consumer('cmd', loop, self.cmd_handler)
        self.cmd_publisher = Publisher('data')
        self.valve = FakeMainValve(0, 30, valve_name, valve_id, 40, 20)
        logger.debug(colorama.Fore.GREEN + f'Valvecontroller {valve_id} setup')
        # asyncio.ensure_future(consumer.run())

    async def start_listen(self):
        await self.consumer.run()

    async def cmd_handler(self, cmd):
        if not cmd['cmd'].startswith(f'{self.valve.valve_id}:'):
            logger.debug(f'Command does not start with motor ID {self.valve.valve_id}. Got {cmd["cmd"]}')
            print(f'fail got {cmd["cmd"]}', f'{self.valve.valve_id}:')
            return

        command = cmd['cmd'][len(self.valve.valve_id) + 1:]

        # logger.info(colorama.Fore.YELLOW + f'{self.motor.motor_id} FakeController got: {command}')
        print(colorama.Fore.YELLOW + f'{self.valve.valve_id} FakeController got: {command}')
        if command == 'start':
            self.valve.open_gas()


async def main():
    loop = asyncio.get_event_loop()
    controller = FakeValveController(loop, 'v1', 'Main valve')
    await controller.start_listen()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    future = loop.create_task(main())
    loop.run_forever()
