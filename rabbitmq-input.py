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
        # cmd = 'foo:m1'
        if cmd == 'exit':
            run = False
        else:
            data = cmd.split(':')
            cmd_publisher.send_msg(data[1], 'cmd', data[0])


if __name__ == '__main__':
    main()
