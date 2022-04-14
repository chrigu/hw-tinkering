import RPi.GPIO as GPIO

pin1 = 14
pin2 = 7
pin3 = 8
pin4 = 16
pin5 = 26
counter = 0


def foo(pin):
    global counter
    counter += 1
    print(f'Event from pin {pin}, counter: {counter}')


def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    # same for pin3 - pin5

    GPIO.add_event_detect(pin1, GPIO.RISING, callback=foo)

    while True:
        pass


if __name__ == '__main__':
    main()