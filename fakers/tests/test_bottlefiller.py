import unittest
from unittest.mock import patch

from web.state_machine import BottleFiller


SENDER = 'sm?'


class TestTriggerMethods(unittest.TestCase):

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    def test_initial_state_off(self, publisher_mock, consumer_mock):
        consumer_mock.return_value = None
        publisher_mock.return_value = None
        filler = BottleFiller(None)
        self.assertEqual('off', filler.state)

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_start(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.start()
        self.assertEqual('opening gas', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_gas')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_open(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('opening gas')
        filler.gas_open()
        self.assertEqual('gas open', filler.state)
        publisher_send_msg.assert_not_called()

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_filled(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('gas open')
        filler.gas_filled()
        self.assertEqual('closing gas', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_gas')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_gas_closed(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('closing gas')
        filler.gas_closed()
        self.assertEqual('opening liquid', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_liquid')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_open(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('opening liquid')
        filler.liquid_open()
        self.assertEqual('liquid open', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_release')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_open(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('opening liquid')
        filler.liquid_open()
        self.assertEqual('liquid open', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'open_release')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_release_open(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('liquid open')
        filler.release_open()
        self.assertEqual('filling liquid', filler.state)
        publisher_send_msg.assert_not_called()

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_filled_with_liquid_open(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('liquid open')
        self._trigger_filled(filler, publisher_send_msg)

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_filled_with_filling_liquid(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('filling liquid')
        self._trigger_filled(filler, publisher_send_msg)

    def _trigger_filled(self, filler, publisher_send_msg):
        filler.filled()
        self.assertEqual('closing release', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_release')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_release_closed(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('closing release')
        filler.release_closed()
        self.assertEqual('closing liquid', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'close_liquid')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_liquid_closed(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('closing liquid')
        filler.liquid_closed()
        self.assertEqual('off', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'shutoff')

    @patch('web.consumer.Consumer.__init__')
    @patch('web.publisher.Publisher.__init__')
    @patch('web.publisher.Publisher.send_msg')
    def test_trigger_abort(self, publisher_send_msg, publisher_init__mock, consumer_init__mock):
        consumer_init__mock.return_value = None
        publisher_init__mock.return_value = None
        filler = BottleFiller(None)
        filler.machine.set_state('filling liquid')
        filler.abort()
        self.assertEqual('off', filler.state)
        publisher_send_msg.assert_called_with(SENDER, 'cmd', 'shutoff')
