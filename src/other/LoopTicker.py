import logging
from timeit import default_timer as timer
import time
from random import random


class LoopTicker:
    def __init__(self, tick_interval_in_seconds):
        self.tick_interval_in_seconds = tick_interval_in_seconds
        self.start = timer()
        self.first_run = True

    def _get_interval(self):  # to look more like a human
        max_incline = 0.15
        current_incline = random() * max_incline
        current_incline_in_seconds = self.tick_interval_in_seconds * current_incline

        if random() > 0.5:
            random_val = self.tick_interval_in_seconds + current_incline_in_seconds
        else:
            random_val = self.tick_interval_in_seconds - current_incline_in_seconds

        return random_val

    def tick(self):
        if self.first_run:
            self.first_run = False
        else:
            end = timer()
            time_passed_in_seconds = end - self.start
            time_left_in_the_interval = self._get_interval() - time_passed_in_seconds
            if time_left_in_the_interval > 0:
                logging.info(f"Going sleep for {time_left_in_the_interval}s")

                time.sleep(time_left_in_the_interval)

            self.start = timer()

        return True
