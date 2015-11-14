import logging
import os
from time import time


class RateLimitingFilter(logging.Filter):
    """
    The RateLimitingFilter is a logging filter that can be used to throttle the number
    of records being sent through a logging handler. Internally the RateLimitingFilter is
    based on an implementation of the the Token Bucket algorithm to restrict the
    throughput of records. The desired throughput can be configured when instantiating
    an instance of the filter.
    """

    def __init__(self, rate=1, per=30, burst=1):
        """
        Create an instance of the RateLimitingFilter allowing a default rate of 1 record
        every 30 seconds when no arguments are supplied.

        :param rate: The number of records to restrict to, per the specified time interval. Default 1.
        :param per: The number of seconds during which 'rate' records may be sent. Default 30.
        :param burst: The maximum number of records that can be sent before rate limiting kicks in.
        """
        super(RateLimitingFilter, self).__init__()

        self._rate = rate
        self._per = per or 1
        self._burst = burst
        self._allowance = burst
        self._limited = 0
        self._last_check = time()

    def filter(self, record):
        """
        Determines whether the supplied record should be logged based upon current rate limits.
        If rate limits have been reached, the record is not logged and a counter is incremented
        to indicate that the record has been throttled. The next time a record is successfully
        logged, the number of previously throttled records is appended to the end of the message.

        :param record: The record to log.
        :return: True if the record can be logged, False otherwise.
        """

        now = time()
        delta = now - self._last_check
        self._last_check = now

        self._allowance += delta * (self._rate / self._per)

        if self._allowance > self._burst:
            self._allowance = self._burst

        if self._allowance < 1:
            # Rate limit
            self._limited += 1

            return False
        else:
            if self._limited > 0:
                # Append a message to the record indicating the number of previously suppressed messages
                record.msg += '{linesep}... {num} additional messages suppressed'.format(linesep=os.linesep,
                                                                                         num=self._limited)
            self._limited = 0
            self._allowance -= 1

            return True
