import logging
import time
from typing import Callable

LOGGER = logging.getLogger(__name__)


class FakeFlowMeter:
    def __init__(self, name: str, valve_id: str, flow_rate: float, flow_cb: Callable[[float, bool], None],
                 initial_volume=0):

        self.volume = initial_volume
        self.name = name
        self.valve_id = valve_id
        self.flow_cb = flow_cb
        self.measure = False
        self.flow_rate = flow_rate

    def measure(self):
        if self.measure:
            return

        self.measure = True

        i = 0

        while self.measure:
            time.sleep(0.1)

            self.volume += self.flow_rate/10
            if i % 10 == 0:
                # logging.debug(f'Fakemotor {self.name} at position {self.position}')
                if self.flow_cb:
                    self.flow_cb(self.volume)

            i += 1


    def stop(self):
        self.measure = False
