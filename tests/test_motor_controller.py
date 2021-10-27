import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from web.fakers.fake_motor_controller import FakeMotorController


VALVE_MOTOR_CONFIG = {
    'name': 'Valve motor',
    'id': 'm1',
    'initial': 0,
    'speed': 30,
    'commands': {
        'open_gas': {
            'speed': 30,
            'position': -90,
            'direction': -1,
            'done': 'gas_open'
        }
    }
}


class TestMotorController(IsolatedAsyncioTestCase):

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        self.mc = FakeMotorController(None, VALVE_MOTOR_CONFIG)

    async def test_ignores_invalid_cmd(self):
        await self.mc.cmd_handler({'data': {'messageType': 'cmd', 'node': VALVE_MOTOR_CONFIG['id'], 'data': 'bla'}})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_message_for_other_node(self):
        cmd = [*VALVE_MOTOR_CONFIG['commands']][0]
        await self.mc.cmd_handler({'data': {'messageType': 'cmd', 'node': 'some', 'data': cmd}})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_invalid_message_type(self):
        cmd = [*VALVE_MOTOR_CONFIG['commands']][0]
        await self.mc.cmd_handler({'data': {'messageType': 'some', 'node': VALVE_MOTOR_CONFIG['id'], 'data': cmd}})
        self.assertEqual({}, self.mc.current_cmd)
