import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, call

from web.fakers.motor_controller import FakeMotorController


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
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': VALVE_MOTOR_CONFIG['id'], 'data': 'bla'})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_message_for_other_node(self):
        cmd = [*VALVE_MOTOR_CONFIG['commands']][0]
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': 'some', 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_invalid_message_type(self):
        cmd = [*VALVE_MOTOR_CONFIG['commands']][0]
        await self.mc.cmd_handler({'messageType': 'some', 'node': VALVE_MOTOR_CONFIG['id'], 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

    @patch('web.fakers.motor.FakeMotor.turn')
    async def test_sends_command_to_motor(self, turn_mock):
        cmd_name = [*VALVE_MOTOR_CONFIG['commands']][0]
        cmd = VALVE_MOTOR_CONFIG['commands'][cmd_name]
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': VALVE_MOTOR_CONFIG['id'], 'data': cmd_name})
        turn_mock.assert_called_with(cmd['position'], cmd['direction'])

    @patch('web.publisher.Publisher.send_msg')
    def test_sends_update_on_motor_update(self, send_mock):
        position = 33.2
        self.mc.motor_position(position, False)
        send_mock.assert_called_with(self.mc.motor.motor_id, 'data', str(position))

    @patch('web.publisher.Publisher.send_msg')
    def test_sends_done_on_motor_update(self, send_mock):
        position = 33.2
        cmd_name = [*VALVE_MOTOR_CONFIG['commands']][0]
        cmd = VALVE_MOTOR_CONFIG['commands'][cmd_name]
        self.mc.current_cmd = cmd

        calls = [call(self.mc.motor.motor_id, 'data', str(position)), call(self.mc.motor.motor_id, 'data', cmd['done'])]
        self.mc.motor_position(position, True)
        send_mock.assert_has_calls(calls)
