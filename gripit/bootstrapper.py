import sys
import getopt

from gripit.app import App
from gripit.config import Config
from gripit.services.gpio_configurator import GPIOConfigrator
from gripit.services.gpio import GPIO


class Bootstrapper:
    def run(self):
        try:
            opts, args = getopt.getopt(sys.argv[1:],
                                       "ails:r:",
                                       ["auto_assignment=",
                                        "immediately=",
                                        "log_data_to_screen=",
                                        "sensors=",
                                        "readings="])
        except getopt.GetoptError:
            print('Usage: sudo python3 main.py [-s ids] [-r times] [-l] [-i] [-a]')
            sys.exit(2)
            return

        for opt, arg in opts:
            if opt in ("-s", "--sensors"):
                Config.sensors_to_read = list(
                    map(lambda sensor_id: int(sensor_id), arg.split(','))
                )
            if opt in ("-r", "--readings"):
                Config.max_readings_count = int(arg)
            if opt in ("-l", "--log_data_to_screen"):
                Config.log_data_to_screen = True
            if opt in ("-i", "--immediately"):
                Config.start_immediately = True
            if opt in ("-a", "--auto_assignment"):
                Config.start_auto_assignment = True

        GPIOConfigrator(GPIO).setup()
        App(GPIO).run()
