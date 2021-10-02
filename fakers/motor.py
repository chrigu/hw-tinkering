import logging
import time
from typing import Callable

LOGGER = logging.getLogger(__name__)


class FakeMotor:
    def __init__(self, initial_position: float, speed: float, name: str, motor_id: str,
                 position_cb: Callable[[float, bool], None]):

        self.position = initial_position
        self.speed = speed  # degrees / second
        self.name = name
        self.turn_done = True
        self.motor_id = motor_id
        self._position_cb = position_cb

    def turn(self, position: float, direction: int, speed=0):  # 1 clockwise, -1 counterclockwise
        if not self.turn_done:
            return

        if speed != 0:
            self.speed = speed

        self.turn_done = False
        i = 0

        while not self.turn_done:
            time.sleep(0.1)

            self.position += direction * self.speed/10
            if i % 10 == 0:
                # logging.debug(f'Fakemotor {self.name} at position {self.position}')
                if self._position_cb:
                    self._position_cb(self.position, self.turn_done)

            if position >= 0:
                self.turn_done = self.position >= position
            else:
                self.turn_done = self.position <= position

            i += 1

        self.position = position
        self._position_cb(self.position, self.turn_done)

    def stop(self):
        self.turn_done = True
