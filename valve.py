import logging

import asyncio

from adafruit_servokit import ServoKit

from consumer import Consumer

# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
from publisher import Publisher

logger = logging.getLogger(__name__)


class MotorBase:
    def __init__(self, motor_id):
        self.kit = ServoKit(channels=16)
        self.motor_id = motor_id
        self.init()

    def init(self):
        raise Exception('MotorBase must be subclassed!')


class Valve(MotorBase):

    def init(self):
        self.neutral()

    def fill_liquid(self):
        self.kit.servo[self.motor_id].angle = 180

    def fill_gas(self):
        self.kit.servo[self.motor_id].angle = 0

    def neutral(self):
        self.kit.servo[self.motor_id].angle = 90


class BlowOff(MotorBase):

    def init(self):
        self.closed()

    def closed(self):
        self.kit.servo[self.motor_id].angle = 0

    def open(self):
        self.kit.servo[self.motor_id].angle = 180
