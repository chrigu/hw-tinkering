import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, call

from web.fakers.motor import FakeMotor
from web.fakers.motor_controller import MotorController


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

    @patch('web.consumer.RabbitConsumer.__init__')
    @patch('web.publisher.RabbitPublisher.send_message')
    @patch('web.publisher.RabbitPublisher.send_message')
    def setUp(self, data_publisher_mock, cmd_publisher_mock, consumer_mock) -> None:
        self.data_publisher_mock = data_publisher_mock
        self.cmd_publisher_mock = cmd_publisher_mock
        self.consumer_mock = consumer_mock
        motor = FakeMotor(VALVE_MOTOR_CONFIG['initial'], VALVE_MOTOR_CONFIG['speed'], VALVE_MOTOR_CONFIG['name'],
                          VALVE_MOTOR_CONFIG['id'])
        self.mc = MotorController(VALVE_MOTOR_CONFIG, self.data_publisher_mock, self.cmd_publisher_mock,
                                  self.consumer_mock, motor)

    async def test_ignores_invalid_cmd(self):
        await self.mc.cmd_handler({'messageType': 'cmd2', 'node': VALVE_MOTOR_CONFIG['id'], 'data': 'bla'})
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

    def test_sends_update_on_motor_update(self):
        position = 33.2
        self.mc.motor_position(position, False)
        self.data_publisher_mock.assert_has_calls([call.send_message(self.mc.motor.motor_id, str(position))])

    def test_sends_done_on_motor_update(self):
        position = 33.2
        cmd_name = [*VALVE_MOTOR_CONFIG['commands']][0]
        cmd = VALVE_MOTOR_CONFIG['commands'][cmd_name]
        self.mc.current_cmd = cmd

        data_calls = [call.send_message(self.mc.motor.motor_id, str(position))]
        cmd_calls = [call.send_message(self.mc.motor.motor_id, cmd['done'])]

        self.mc.motor_position(position, True)
        self.cmd_publisher_mock.assert_has_calls(cmd_calls)
        self.data_publisher_mock.assert_has_calls(data_calls)
