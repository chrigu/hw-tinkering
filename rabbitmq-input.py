import logging
import sys

import asyncio

# from adafruit_servokit import ServoKit

# https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library
from publisher import Publisher

logger = logging.getLogger(__name__)


def main():
    run = True
    cmd_publisher = Publisher('data')
    # cmd_publisher.send_msg('fm1', 'cmd', '34')
    while run:
        cmd = input("Enter command: ")
        if cmd == 'exit':
            run = False
        else:
            # data = cmd.split(':')
            # cmd_publisher.send_msg(data[0], 'cmd', data[1])
            cmd_publisher.send_msg('data', 'some', cmd)


if __name__ == '__main__':
    main()
