from adafruit_servokit import ServoKit
from typing import Callable

i2c = busio.I2C(board.SCL, board.SDA)
hat = adafruit_pca9685.PCA9685(i2c)

LOGGER = logging.getLogger(__name__)

# https://circuitpython.readthedocs.io/projects/servokit/en/latest/

class Motor:
    def __init__(self, initial_position: float, speed: float, name: str, motor_id: str,
                 position_cb: Callable[[float, bool], None]):

        self.position = initial_position
        self.speed = speed  # degrees / second
        self.name = name
        self.turn_done = True
        self.motor_id = motor_id
        self._position_cb = position_cb
        self.kit = ServoKit(channels=16)

        self._turn()

    def turn(self, position: float, direction: int, speed=0):  # 1 clockwise, -1 counterclockwise
        if not self.turn_done:
            return

        if speed == 0:
            self.speed = speed

        self.turn_done = False
        self.position = position
        self._turn()

        self.position = position
        self._position_cb(self.position, self.turn_done)

    def _turn(self):
        self.kit.servo[0].angle = self.position

    def stop(self):
        self.turn_done = True
