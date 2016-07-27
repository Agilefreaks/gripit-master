import time

class TimeService:
    def current_milli_time(self):
        return int(round(time.time() * 1000))
