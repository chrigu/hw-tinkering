import logging
import sys

import asyncio

# from adafruit_servokit import ServoKit

# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
from publisher import Publisher

logger = logging.getLogger(__name__)


def main():
    run = True
    cmd_publisher = Publisher('cmd')
    while run:
        cmd = input("Enter command: ")
        # cmd = 'm1:foo'
        if cmd == 'exit':
            run = False
        else:
            cmd_publisher.send_msg(cmd)


if __name__ == '__main__':
    main()
