import logging
import time

from web.fakers.motor import FakeMotor

LOGGER = logging.getLogger(__name__)

GAS_POSITION = -90
NEUTRAL_POSITION = 0
LIQUID_POSITION = 90


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

    def open_gas(self):
        print(f'Opening gas')
        self.set_motor_position = GAS_POSITION
        self._time = time.time()
        self.motor.turn(self.set_motor_position, -1)

    def motor_position(self, position: float, done: bool) -> None:
        delta = time.time() - self._time
        print(f'Fakemotor {self.motor.motor_id} at position {position} with dt {delta}')
        self._time = time.time()

    def calc_flow(self, speed: float, max_value: float, current_value: float, dt: float) -> float:

