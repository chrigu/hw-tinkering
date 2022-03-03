import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch, call

from web.state_machine import BottleFiller


SENDER = 'sm?'


class TestTriggerMethods(unittest.TestCase):
    
    @patch('web.consumer.RabbitConsumer.__init__')
    @patch('web.publisher.RabbitPublisher.send_message')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.filler = BottleFiller(SENDER, self.consumer_mock, self.consumer_mock, self.publisher_mock)

    def test_initial_state_off(self):
        self.assertEqual('off', self.filler.state)

    def test_trigger_start(self):
        self.filler.start()
        self.assertEqual('opening gas', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'open_gas')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_gas_open(self):
        self.filler.machine.set_state('opening gas')
        self.filler.gas_open()
        self.assertEqual('gas open', self.filler.state)
        self.publisher_mock.assert_not_called()

    def test_trigger_gas_filled(self):
        self.filler.machine.set_state('gas open')
        self.filler.gas_filled()
        self.assertEqual('closing gas', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'close_gas')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_gas_closed(self):
        self.filler.machine.set_state('closing gas')
        self.filler.gas_closed()
        self.assertEqual('opening liquid', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'open_liquid')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_liquid_open(self):
        self.filler.machine.set_state('opening liquid')
        self.filler.liquid_open()
        self.assertEqual('liquid open', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'open_release')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_release_open(self):
        self.filler.machine.set_state('liquid open')
        self.filler.release_open()
        self.assertEqual('filling liquid', self.filler.state)
        self.publisher_mock.assert_not_called()

    def test_trigger_filled_with_liquid_open(self):
        self.filler.machine.set_state('liquid open')
        self._trigger_filled(self.filler)

    def test_trigger_filled_with_filling_liquid(self):
        self.filler.machine.set_state('filling liquid')
        self._trigger_filled(self.filler)

    def _trigger_filled(self, filler):
        filler.filled()
        self.assertEqual('closing release', filler.state)
        cmd_call = [call.send_message(SENDER, 'close_release')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_release_closed(self):
        self.filler.machine.set_state('closing release')
        self.filler.release_closed()
        self.assertEqual('closing liquid', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'close_liquid')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_liquid_closed(self):
        self.filler.machine.set_state('closing liquid')
        self.filler.liquid_closed()
        self.assertEqual('off', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'shutoff')]
        self.publisher_mock.assert_has_calls(cmd_call)

    def test_trigger_abort(self):
        self.filler.machine.set_state('filling liquid')
        self.filler.abort()
        self.assertEqual('off', self.filler.state)
        cmd_call = [call.send_message(SENDER, 'shutoff')]
        self.publisher_mock.assert_has_calls(cmd_call)


class TestDataHandler(IsolatedAsyncioTestCase):

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        self.filler = BottleFiller(None, 'sm')

    @patch('web.state_machine.BottleFiller.call_trigger')
    async def test_handle_valid_command(self, start_mock):
        await self.filler.data_handler({'messageType': 'data', 'data': 'start'})
        self.assertEqual('off', self.filler.state)
        start_mock.assert_called_with('start')

    @patch('web.state_machine.BottleFiller.call_trigger')
    async def test_handle_invalid_command(self, start_mock):
        await self.filler.data_handler({'messageType': 'data', 'data': 'asdfasdf'})
        self.assertEqual('off', self.filler.state)
        start_mock.assert_not_called()
