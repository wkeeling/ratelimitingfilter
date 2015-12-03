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

    def __init__(self, rate=1, per=30, burst=1, **kwargs):
        """
        Create an instance of the RateLimitingFilter allowing a default rate of 1 record
        every 30 seconds when no arguments are supplied.

        :param rate: The number of records to restrict to, per the specified time interval. Default 1.
        :param per: The number of seconds during which 'rate' records may be sent. Default 30.
        :param burst: The maximum number of records that can be sent before rate limiting kicks in.
        :param kwargs: Additional config options that can be passed to the filter.
        """
        super(RateLimitingFilter, self).__init__()

        self._default_bucket = TokenBucket(rate, per, burst)
        self._substr_buckets = {}
        self._auto_buckets = {}

        if 'match' in kwargs:
            if kwargs['match'] != 'auto':
                for s in kwargs['match']:
                    self._substr_buckets[s] = TokenBucket(rate, per, burst)

    def filter(self, record):
        """
        Determines whether the supplied record should be logged based upon current rate limits.
        If rate limits have been reached, the record is not logged and a counter is incremented
        to indicate that the record has been throttled. The next time a record is successfully
        logged, the number of previously throttled records is appended to the end of the message.

        :param record: The record to log.
        :return: True if the record can be logged, False otherwise.
        """

        bucket = self._bucket(record)

        if not bucket:
            return True

        if bucket.consume():
            if bucket.limited > 0:
                # Append a message to the record indicating the number of previously suppressed messages
                record.msg += '{linesep}... {num} additional messages suppressed'.format(linesep=os.linesep,
                                                                                         num=bucket.limited)
            bucket.limited = 0
            return True
        else:
            # Rate limit
            bucket.limited += 1
            return False

    def _bucket(self, record):
        bucket = None

        if self._substr_buckets:
            # Locate the relevant token bucket by matching the substrings against the message
            for substr in self._substr_buckets:
                if substr in record.msg:
                    bucket = self._substr_buckets[substr]
                    break
        elif self._auto_buckets:
            pass
        else:
            bucket = self._default_bucket

        return bucket  # May be None which implies no filtering


class TokenBucket(object):

    def __init__(self, rate, per, burst):
        self._rate = rate
        self._per = per or 1
        self._burst = burst
        self._allowance = burst
        self._last_check = time()
        self.limited = 0

    def consume(self):
        now = time()
        delta = now - self._last_check
        self._last_check = now

        self._allowance += delta * (self._rate / self._per)

        if self._allowance > self._burst:
            self._allowance = self._burst

        if self._allowance < 1:
            return False
        else:
            self._allowance -= 1
            return True
