import time
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from web.fakers.flow_controller import FlowMeterController
from web.fakers.flowmeter import FakeFlowMeter


FLOWMETER_CONFIG = {
    'name': 'Gas in flowmeter',
    'id': 'fm1',
    'flowrate': 30, # only for fake
    'trigger_command': 'open_gas',
    'state_machine_id': 'sm',
    'threshold': {
        'value': 100,
        'command': 'close_valve',
        'difference': 100
    }
}


class TestFlowController(IsolatedAsyncioTestCase):

    @patch('web.consumer.RabbitConsumer.__init__')
    @patch('web.publisher.RabbitPublisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        flowmeter = FakeFlowMeter(FLOWMETER_CONFIG['name'], FLOWMETER_CONFIG['id'],
                                  FLOWMETER_CONFIG['flowrate'])
        self.mc = FlowMeterController(FLOWMETER_CONFIG, self.publisher_mock, self.publisher_mock, self.consumer_mock,
                                      flowmeter)

    async def test_ignores_invalid_cmd(self):
        await self.mc.cmd_handler({'messageType': 'cmd', 'node': FLOWMETER_CONFIG['id'], 'data': 'bla'})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_message_for_other_node(self):
        cmd = FLOWMETER_CONFIG['trigger_command']
        await self.mc.cmd_handler({'messageType': 'cmd2', 'node': 'some', 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

    async def test_ignores_invalid_message_type(self):
        cmd = FLOWMETER_CONFIG['trigger_command']
        await self.mc.cmd_handler({'messageType': 'some', 'node': FLOWMETER_CONFIG['id'], 'data': cmd})
        self.assertEqual({}, self.mc.current_cmd)

    def test_no_pulses_and_timeout(self):
        self.mc.time = time.time() - 1.5
        self.assertTrue(self.mc.check_pulses(0))

    def test_no_pulses_no_timeout(self):
        self.mc.time = time.time() - 1.0
        self.assertFalse(self.mc.check_pulses(0))

    def test_pulses(self):
        self.mc.time = time.time() - 1.0
        self.assertFalse(self.mc.check_pulses(200))
