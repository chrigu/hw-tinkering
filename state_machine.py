from enum import Enum

class ValveState(Enum):
    NEUTRAL = 0
    FILL_GAS = 1
    FILL_LIQUID = 2


class BlowoffState(Enum):
    OFF = False
    ON = True


class FillState(Enum):
    OFF = 0
    OPENING_GAS = 1
    GAS_OPEN = 2
    CLOSING_GAS = 3
    OPENING_LIQUID = 4
    LIQUID_OPEN = 5
    OPENING_RELEASE = 6
    FILLING = 7
    CLOSING_RELEASE = 8
    RELEASE_CLOSED = 9
    CLOSING_LIQUID = 10
    TRI_NEUTRAL = 11


class Events(Enum):
    START = 'start'
    STOP = 'stop'
    GAS_OPEN = 'gas_open'
    GAS_FILLED = 'gas_filled'
    GAS_CLOSED = 'gas_closed'
    LIQUID_OPEN = 'liquid_open'
    LIQUID_FILLED = 'liquid_filled'
    LIQUID_CLOSED = 'liquid_closed'
    RELEASE_OPEN = 'release_open'
    RELEASE_CLOSED = 'release_closed'
    TRI_NEUTRAL = 'tri_neutral'


def state_machine(event: Events, state: FillState) -> FillState:
    if state == FillState.OFF:
        if event == Events.START:
            return FillState.OPENING_GAS

            # actions: open gas, measure gas

    elif state == FillState.OPENING_GAS:
        if event == Events.GAS_OPEN:
            return FillState.GAS_OPEN

            # actions: measure gas

    elif state == FillState.GAS_OPEN:
        if event == Events.GAS_FILLED:
            return FillState.CLOSING_GAS

            # actions: close gas & mesure

    elif state == FillState.CLOSING_GAS:
        if event == Events.TRI_NEUTRAL:
            return FillState.OPENING_LIQUID

            # actions: open liquid & measure liquid

    elif state == FillState.OPENING_LIQUID:
        if event == Events.LIQUID_OPEN:
            return FillState.OPENING_RELEASE

            # actions: open liquid & measure liquid

    elif state == FillState.OPENING_RELEASE:
        if event == Events.RELEASE_OPEN:
            return FillState.FILLING

            # actions:  measure liquid

    elif state == FillState.FILLING:
        if event == Events.LIQUID_FILLED:
            return FillState.CLOSING_RELEASE

            # actions: close release & measure liquid

    elif state == FillState.CLOSING_RELEASE:
        if event == Events.RELEASE_CLOSED:
            return FillState.CLOSING_LIQUID

            # actions: close release & measure liquid

    elif state == FillState.CLOSING_LIQUID:
        if event == Events.LIQUID_CLOSED:
            return FillState.OFF

    # add stop states