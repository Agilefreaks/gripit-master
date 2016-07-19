try:
    import RPi.GPIO as RPI_GPIO
    IMPORT_FAILED = False
except ImportError:
    IMPORT_FAILED = True


class GPIO:

    if IMPORT_FAILED:
        BCM = None

        OUT = 0
        IN = 1
        HIGH = True
        LOW = False

        RISING = 1
        FALLING = 2
        BOTH = 3

        PUD_OFF = 0
        PUD_DOWN = 1
        PUD_UP = 2
    else:
        BCM = RPI_GPIO.BCM

        OUT = RPI_GPIO.OUT
        IN = RPI_GPIO.IN
        HIGH = RPI_GPIO.HIGH
        LOW = RPI_GPIO.LOW

        RISING = RPI_GPIO.RISING
        FALLING = RPI_GPIO.FALLING
        BOTH = RPI_GPIO.BOTH

        PUD_OFF = RPI_GPIO.PUD_OFF
        PUD_DOWN = RPI_GPIO.PUD_DOWN
        PUD_UP = RPI_GPIO.PUD_UP

    def setmode(self, param):
        if IMPORT_FAILED:
            return 0
        RPI_GPIO.setmode(GPIO.BCM)

    def setwarnings(self, param):
        if IMPORT_FAILED:
            return 0
        RPI_GPIO.setwarnings(param)

    def setup(self, gpio, direction, **pull_up_down):
        if IMPORT_FAILED:
            return 0
        RPI_GPIO.setup(gpio, direction, **pull_up_down)

    def output(self, gpio, value):
        if IMPORT_FAILED:
            return 0
        RPI_GPIO.output(gpio, value)

    def add_event_detect(self, gpio, value, **callback):
        if IMPORT_FAILED:
            return 0
        RPI_GPIO.add_event_detect(gpio, value, **callback)
