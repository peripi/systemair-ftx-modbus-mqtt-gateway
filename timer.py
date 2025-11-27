from time import time

class Timer():
    def __init__(self):
        self._ts_start = None
        self.start()

    def start(self):
        self._ts_start = time()

    def elapsed_time(self)->tuple:
        """
        Elapsed time as (days, hours, minutes, seconds)
        :return:
        """
        elapsed = time() - self._ts_start
        days = int(elapsed/(3600*24))
        elapsed = elapsed % (3600*24)
        hours = int(elapsed/3600)
        elapsed = elapsed % 3600
        minutes = int(elapsed/60)
        seconds = elapsed % 60
        return days, hours, minutes, seconds

