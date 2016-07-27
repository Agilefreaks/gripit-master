class Config:
    LED_PIN = 2
    BUTTON_PIN = 26

    FIRST_SLAVE_ADDRESS = 1
    LAST_SLAVE_ADDRESS = 5

    FIRST_REGISTER_ADDRESS = 1
    LAST_REGISTER_ADDRESS = 4

    MODBUS_CLIENT_KWARGS = {
        "method": "rtu",
        "stopbits": 1,
        "bytesize": 8,
        "parity": "N",
        "baudrate": 115200,
        "port": "/dev/ttyUSB0",
        "timeout": 0.02
    }

    sensors_to_read = range(FIRST_SLAVE_ADDRESS,
                            LAST_SLAVE_ADDRESS + 1)
    max_readings_count = float('inf')
    log_data_to_screen = False
    start_immediately = False
