import logging
from time import time


class RateLimitingHandler(logging.Handler):

    def __init__(self, target, rate=1, per=30, burst=1):
        super(RateLimitingHandler, self).__init__()

        self._target = target
        self._rate = rate
        self._per = per
        self._burst = burst
        self._allowance = burst
        self._limited = 0
        self._last_check = time()

    def emit(self, record):
        now = time()
        delta = now - self._last_check
        self._last_check = now

        self._allowance += delta * (self._rate / self._per)

        if self._allowance > self._burst:
            self._allowance = self._burst

        if self._allowance < 1:
            # Rate limit
            self._limited += 1
        else:
            self._target.emit(record)
            self._allowance -= 1



