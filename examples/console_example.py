import logging
import time

from ratelimitingfilter import RateLimitingFilter


logger = logging.getLogger('console_example')
logger.setLevel(logging.DEBUG)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

# Create a rate limiting filter and add it to the console handler.
# We limit the throughput to 1 record per second, allowing a burst of 3.
throttle = RateLimitingFilter(rate=1, per=1, burst=3)
ch.addFilter(throttle)

for i in range(31):
    # This attempts to log 31 messages in a little over 3 seconds. The messages are equally
    # spaced with 1/10 second between them. This allows the first 3 messages through in the
    # first second based on the burst, and then just 1 message in the 2nd, 3rd and 4th seconds,
    # based on the 1 per second rate, which totals 6.
    logger.debug('This is message {0}'.format(i))
    time.sleep(0.1)
