import logging
import time
from typing import Callable, List

LOGGER = logging.getLogger(__name__)
TIME_DELTA = 0.1


class FakeFlowMeter:
    def __init__(self, name: str, meter_id: str, flow_rates: List[dict], initial_pulses=0):

        self.pulses = initial_pulses
        self.name = name
        self.meter_id = meter_id
        self.is_measuring = False
        self.flow_rates = flow_rates
        self.flow_cb = None

    def set_flow_cb(self, flow_cb: Callable[[int, int], None]):
        self.flow_cb = flow_cb

    def measure(self):
        if self.is_measuring:
            return

        self.is_measuring = True

        i = 0

        while self.is_measuring:
            for flow_rate in self.flow_rates:
                duration = flow_rate['duration']
                elapsed = 0
                while elapsed < duration:
                    time.sleep(TIME_DELTA)
                    elapsed += TIME_DELTA

                    self.pulses += flow_rate['pulses']
                    # logging.debug(f'Fakemotor {self.name} at position {self.position}')
                    if self.flow_cb:
                        self.flow_cb(self.pulses, flow_rate['pulses'])

                    i += 1

    def stop(self):
        self.is_measuring = False
