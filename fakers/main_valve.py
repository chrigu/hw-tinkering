import logging
import time
from enum import Enum

from web.fakers.motor import FakeMotor

logger = logging.getLogger(__name__)

GAS_POSITION = -90
NEUTRAL_POSITION = 0
LIQUID_POSITION = 90


class ValveState(Enum):
    NEUTRAL = 0
    GAS_OPEN = 1
    LIQUID_OPEN = 2


# use state machine
"""
        {'trigger': 'gas_open', 'source': 'opening gas', 'dest': 'gas open', 'on_enter': ['open_gas']},
        {'trigger': 'gas_filled', 'source': 'gas open', 'dest': 'closing gas'},
        {'trigger': 'gas_closed', 'source': 'closing gas', 'dest': 'opening liquid'},
        {'trigger': 'liquid_open', 'source': 'opening liquid', 'dest': 'liquid open'},
"""

class FakeMainValve:
    """
    gas_speed = cm3 / s
    """
    def __init__(self, initial_position: float, motor_speed: float, name: str, valve_id: str,
                 gas_speed: float, liquid_speed: float):

        self.position = initial_position
        self.motor_speed = motor_speed  # degrees / second
        self.name = name
        self.turn_done = True
        self.valve_id = valve_id
        self.gas_speed = gas_speed
        self.liquid_speed = liquid_speed
        self.motor = FakeMotor(0, 50, 'Valve motor', 'm1', self.motor_position)
        self._gas_volume = 0
        self._liquid_volume = 0
        self.set_motor_position = 0
        self._time = 0
        self.state = ValveState.NEUTRAL

    def open_gas(self):
        logger.debug(f'Opening gas')
        self.state = ValveState.LIQUID_OPEN
        self.set_motor_position = GAS_POSITION
        self._time = time.time()
        self.motor.turn(self.set_motor_position, -1)

    def open_liquid(self):
        logger.debug(f'Opening liquid')
        self.set_motor_position = LIQUID_POSITION
        self._time = time.time()
        self.motor.turn(self.set_motor_position, 1)

    def motor_position(self, position: float, done: bool) -> None:
        delta = time.time() - self._time
        self._gas_volume += self.calc_flow_volume(self.gas_speed, GAS_POSITION, position, delta)

        print(f'Fakemotor {self.motor.motor_id} at position {position} with dt {delta}')
        print(f'Gas volume at {self._gas_volume}cm3')
        self._time = time.time()

    def calc_flow_volume(self, speed: float, max_value: float, current_value: float, dt: float) -> float:
        factor = current_value / max_value
        return factor * dt * speed
