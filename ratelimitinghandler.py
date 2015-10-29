import logging


class RateLimitingHandler(logging.Handler):

    def __init__(self, rate=1, per=30, burst=1):
        super(RateLimitingHandler, self).__init__()