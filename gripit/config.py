class Config:
    LED_PIN = 2
    BUTTON_PIN = 26

    FIRST_REGISTER_ADDRESS = 1
    LAST_REGISTER_ADDRESS = 4

    NUMBER_OF_SLAVES_ON_BUS = 2

    MIN_SLAVE_ADDRESS = 1
    MAX_SLAVE_ADDRESS = 32

    SLAVE_ID_REGISTER_ADDRESS = 5

    FORCE_GENERATE_ID_REGISTER_ADDRESS = 6
    AUTO_ASSIGNMENT_MODE_REGISTER_ADDRESS = 7

    AUTO_ASSIGNMENT_MODE_ON = 1
    AUTO_ASSIGNMENT_MODE_OFF = 0

    REGENERATE_ID_COMMAND = 1

    MAX_REGISTER_ADDRESS = 255

    MODBUS_CLIENT_KWARGS = {
        "method": "rtu",
        "stopbits": 1,
        "bytesize": 8,
        "parity": "N",
        "baudrate": 115200,
        "port": "/dev/ttyUSB0",
        "timeout": 0.02
    }

    sensors_to_read = range(MIN_SLAVE_ADDRESS,
                            MAX_SLAVE_ADDRESS + 1)
    max_readings_count = float('inf')
    log_data_to_screen = False
    start_immediately = False
    start_auto_assignment = False
    reading_sleep_time = 0.0005
