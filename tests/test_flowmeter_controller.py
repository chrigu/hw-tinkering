import asyncio
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, call

from web.fakers.flow_controller import FakeFlowMeterController
from web.fakers.motor_controller import FakeMotorController


FLOWMETER_CONFIG = {
    'name': 'Gas in flowmeter',
    'id': 'fm1',
    'flowrate': 30, #only for faek
    'trigger_command': 'open_gas',
    'threshold': {
        'value': 100,
        'command': 'close_valve'
    }
}


class TestFlowController(IsolatedAsyncioTestCase):

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        self.mc = FakeFlowMeterController(None, FLOWMETER_CONFIG)

    async def test_ignores_invalid_cmd(self):
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': FLOWMETER_CONFIG['id'], 'data': 'bla'})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_message_for_other_node(self):
        cmd = FLOWMETER_CONFIG['trigger_command']
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': 'some', 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_invalid_message_type(self):
        cmd = FLOWMETER_CONFIG['trigger_command']
        await self.mc.cmd_handler({'messageType': 'some', 'node': FLOWMETER_CONFIG['id'], 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

