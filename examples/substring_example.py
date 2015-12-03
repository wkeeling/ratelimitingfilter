import logging
import time

from ratelimitingfilter import RateLimitingFilter


logger = logging.getLogger('substring_example')
logger.setLevel(logging.DEBUG)

# Create a console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
logger.addHandler(ch)

# Create a rate limiting filter and add it to the console handler.
config = {'match': ['rate limited']}
throttle = RateLimitingFilter(rate=1, per=1, burst=1, **config)
ch.addFilter(throttle)

for i in range(31):
    # Rate limiting will apply to this message because of the substring match
    logger.debug('a message that is rate limited')
    # Rate limiting will not apply to this message
    logger.debug('some message')
    time.sleep(0.1)
