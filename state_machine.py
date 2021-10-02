from enum import Enum
from transitions import Machine

from web.publisher import Publisher


class BlowoffState(Enum):
    OFF = False
    ON = True

MOTOR_CONFIG = {
    'main_valve': 'm1',
    'blowoff': 'm2',
    'gas_input': 'v1',
    'gas_output': 'v2'
}


class FillState(Enum):
    OFF = 0
    OPENING_GAS = 1
    GAS_OPEN = 2
    CLOSING_GAS = 3
    OPENING_LIQUID = 4
    LIQUID_OPEN = 5
    OPENING_RELEASE = 6
    FILLING = 7
    CLOSING_RELEASE = 8
    RELEASE_CLOSED = 9
    CLOSING_LIQUID = 10
    TRI_NEUTRAL = 11


class BottleFiller(object):

    states = [
        'off',
        'opening gas',
        'gas open',
        'closing gas',
        'opening liquid',
        'liquid open',
        'opening release',
        'filling liquid',
        'closing release',
        'closing liqiud',
        'tri neutral',
    ]

    transitions = [
        {'trigger': 'start', 'source': 'off', 'dest': 'opening gas'},
        {'trigger': 'gas_open', 'source': 'opening gas', 'dest': 'gas open', 'on_enter': ['open_gas']},
        {'trigger': 'gas_filled', 'source': 'gas open', 'dest': 'closing gas'},
        {'trigger': 'gas_closed', 'source': 'closing gas', 'dest': 'opening liquid'},
        {'trigger': 'liquid_open', 'source': 'opening liquid', 'dest': 'liquid open'},
        {'trigger': 'opening_release', 'source': 'liquid open', 'dest': 'filling liquid'},
        {'trigger': 'release_open', 'source': 'filling liquid', 'dest': 'filling liquid'},
        {'trigger': 'filled', 'source': 'filling liquid', 'dest': 'closing release'},
        {'trigger': 'release_closed', 'source': 'closing_release', 'dest': 'closing liquid'},
        {'trigger': 'liquid_closed', 'source': 'closing liquid', 'dest': 'off'},
    ]

    def __init__(self):
        self.machine = Machine(model=self, states=BottleFiller.states, transitions=self.transitions, initial='off')
        self.cmd_publisher = Publisher('cmd')

    def open_gas(self):
        print('open gas')

    @property
    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")
