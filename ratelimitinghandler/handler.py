import logging
import os
from time import time


class RateLimitingHandler(logging.Handler):
    """
    The RateLimitingHandler is a logging handler designed to wrap a target handler
    and throttle the number of logging records sent through to that target. Internally
    it is based on an implementation of the the Token Bucket algorithm to restrict the
    throughput of records. The desired throughput can be configured when instantiating
    an instance of the handler.
    """

    def __init__(self, target, rate=1, per=30, burst=1):
        """
        Create an instance of the RateLimitingHandler.

        :param target: The target handler which will receive records after rate limiting.
        :param rate: The number of records to restrict to, per the specified time interval. Default 1.
        :param per: The number of seconds during which 'rate' records may be sent. Default 30.
        :param burst: The maximum number of records that can be sent before rate limiting kicks in.
        """
        super(RateLimitingHandler, self).__init__()

        self._target = target
        self._rate = rate
        self._per = per or 1
        self._burst = burst
        self._allowance = burst
        self._limited = 0
        self._last_check = time()

    def emit(self, record):
        """
        Emits the supplied record by forwarding onto the target handler, provided that rate limits
        have not been reached. If rate limits have been reached, the record is not forwarded but a
        counter is incremented to indicate that a message has been throttled. The next time a record
        is successfully forwarded, the number of previously throttled messages is appended to the
        end of the message.

        :param record: The record to emit.
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
        else:
            if self._limited > 0:
                # Append a message to the record indicating the number of previously suppressed messages
                record.msg += '{linesep}... {num} additional messages suppressed'.format(linesep=os.linesep,
                                                                                         num=self._limited)
            self._target.emit(record)

            self._limited = 0
            self._allowance -= 1
