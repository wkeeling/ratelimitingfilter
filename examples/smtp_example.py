import logging.handlers
import time

from ratelimitingfilter import RateLimitingFilter

logger = logging.getLogger('throttled_smtp_example')

# Create an SMTPHandler
smtp = logging.handlers.SMTPHandler(mailhost='relay.somehost.net',
                                    fromaddr='will@mailinator.com',
                                    toaddrs='will@mailinator.com',
                                    subject='An error has occurred')
smtp.setLevel(logging.ERROR)

# Create an instance of the RateLimitingFilter, and add it to the handler
throttle = RateLimitingFilter()
smtp.addFilter(throttle)

# Create a formatter and set it on the handler
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
smtp.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(smtp)

# Logged errors will now be restricted to 1 every 30 seconds
while True:
    logger.error('An error message')
    time.sleep(2)

