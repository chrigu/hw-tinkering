import unittest
from unittest import IsolatedAsyncioTestCase
from unittest.mock import patch

from web.state_machine import BottleFiller


SENDER = 'sm?'


class TestTriggerMethods(unittest.TestCase):
    
    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        self.filler = BottleFiller(None)

    def test_initial_state_off(self):
        self.assertEqual('off', self.filler.state)

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_start(self, publisher_send_msg):
        self.filler.start()
        self.assertEqual('opening gas', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_gas')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_open(self, publisher_send_msg):
        self.filler.machine.set_state('opening gas')
        self.filler.gas_open()
        self.assertEqual('gas open', self.filler.state)
        publisher_send_msg.assert_not_called()

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_filled(self, publisher_send_msg):
        self.filler.machine.set_state('gas open')
        self.filler.gas_filled()
        self.assertEqual('closing gas', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_gas')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_closed(self, publisher_send_msg):
        self.filler.machine.set_state('closing gas')
        self.filler.gas_closed()
        self.assertEqual('opening liquid', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_liquid')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_open(self, publisher_send_msg):
        self.filler.machine.set_state('opening liquid')
        self.filler.liquid_open()
        self.assertEqual('liquid open', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_release')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_open(self, publisher_send_msg):
        self.filler.machine.set_state('opening liquid')
        self.filler.liquid_open()
        self.assertEqual('liquid open', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_release')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_release_open(self, publisher_send_msg):
        self.filler.machine.set_state('liquid open')
        self.filler.release_open()
        self.assertEqual('filling liquid', self.filler.state)
        publisher_send_msg.assert_not_called()

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_filled_with_liquid_open(self, publisher_send_msg):
        self.filler.machine.set_state('liquid open')
        self._trigger_filled(self.filler, publisher_send_msg)

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_filled_with_filling_liquid(self, publisher_send_msg):
        self.filler.machine.set_state('filling liquid')
        self._trigger_filled(self.filler, publisher_send_msg)

    def _trigger_filled(self, filler, publisher_send_msg):
        filler.filled()
        self.assertEqual('closing release', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_release')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_release_closed(self, publisher_send_msg):
        self.filler.machine.set_state('closing release')
        self.filler.release_closed()
        self.assertEqual('closing liquid', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_liquid')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_closed(self, publisher_send_msg):
        self.filler.machine.set_state('closing liquid')
        self.filler.liquid_closed()
        self.assertEqual('off', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'shutoff')

    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_abort(self, publisher_send_msg):
        self.filler.machine.set_state('filling liquid')
        self.filler.abort()
        self.assertEqual('off', self.filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'shutoff')


class TestDataHandler(IsolatedAsyncioTestCase):

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def setUp(self, publisher_mock, consumer_mock) -> None:
        self.publisher_mock = publisher_mock
        self.consumer_mock = consumer_mock
        self.consumer_mock.return_value = None
        self.publisher_mock.return_value = None
        self.filler = BottleFiller(None)

    # @patch('web.state_machine.BottleFiller.call_trigger')
    # def test_handle_start(self, start_mock):
    #     await self.filler.data_handler({'messageType': 'data', 'data': 'start'})
    #     self.assertEqual('off', self.filler.state)
    #     start_mock.assert_called()

    @patch('web.state_machine.BottleFiller.call_trigger')
    async def test_handle_start(self, start_mock):
        await self.filler.data_handler({'messageType': 'data', 'data': 'start'})
        self.assertEqual('off', self.filler.state)
        start_mock.assert_called_with('start')

# {'trigger': 'start', 'source': 'off', 'dest': 'opening gas'},
# {'trigger': 'gas_open', 'source': 'opening gas', 'dest': 'gas open'},
# {'trigger': 'gas_filled', 'source': 'gas open', 'dest': 'closing gas'},
# {'trigger': 'gas_closed', 'source': 'closing gas', 'dest': 'opening liquid'},
# {'trigger': 'liquid_open', 'source': 'opening liquid', 'dest': 'liquid open'},
# {'trigger': 'release_open', 'source': 'liquid open', 'dest': 'filling liquid'},
# {'trigger': 'filled', 'source': ['filling liquid', 'liquid open'], 'dest': 'closing release'},
# {'trigger': 'release_closed', 'source': 'closing release', 'dest': 'closing liquid'},
# {'trigger': 'liquid_closed', 'source': 'closing liquid', 'dest': 'off'},
# {'trigger': 'abort', 'source': '*', 'dest': 'off'},