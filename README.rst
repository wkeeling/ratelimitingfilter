RateLimitingFilter
==================

.. image:: https://travis-ci.org/wkeeling/ratelimitingfilter.svg?branch=master
        :target: https://travis-ci.org/wkeeling/ratelimitingfilter

.. image:: https://codecov.io/gh/wkeeling/ratelimitingfilter/branch/master/graph/badge.svg
        :target: https://codecov.io/gh/wkeeling/ratelimitingfilter

.. image:: https://img.shields.io/badge/python-2.7%2C%203.4%2C%203.5%2C%203.6%2C%203.7-blue.svg
        :target: https://pypi.python.org/pypi/ratelimitingfilter

.. image:: https://img.shields.io/pypi/v/ratelimitingfilter.svg
        :target: https://pypi.python.org/pypi/ratelimitingfilter

.. image:: https://img.shields.io/pypi/l/ratelimitingfilter.svg
        :target: https://pypi.python.org/pypi/ratelimitingfilter


The ``RateLimitingFilter`` is a filter for the Python logging system
that allows you to restrict the rate at which messages can pass through
your logging handlers.

The filter can be useful if you're using a handler such as Python's
``logging.handlers.SMTPHandler`` to send error notification emails.
Error notification emails provide a useful means of keeping an eye on
the health of a running system, but these emails have the potential to
overload a mailbox if they start arriving in quick succession due to
some kind of critical failure.

The ``RateLimitingFilter`` can help prevent mailbox overload by
throttling messages based on a configurable rate, whilst allowing for
periodic bursts of messages which can be a useful indicator that
something somewhere has broken.

Compatibility
-------------

* Python 2.7, 3.4+

Installing
----------

::

    $ pip install ratelimitingfilter

or

::

    $ git clone https://github.com/wkeeling/ratelimitingfilter.git
    $ cd ratelimitingfilter
    $ python setup.py install

Usage
-----

You can rate-limit a logging handler simply by creating a new instance of the
``RateLimitingFilter`` and adding it to the handler:

.. code:: python

    from ratelimitingfilter import RateLimitingFilter

    ...

    ratelimit = RateLimitingFilter()
    handler.addFilter(ratelimit)

Creating an instance of the ``RateLimitingFilter`` without any arguments
like in the example above will restrict the flow of messages to 1 every
30 seconds.

You can customize the flow rate by supplying your own values for the
``rate``, ``per`` and ``burst`` attributes. For example, to allow a rate
of 1 message every 2 minutes with a periodic burst of up to 5 messages:

.. code:: python

    ratelimit = RateLimitingFilter(rate=1, per=120, burst=5)
    handler.addFilter(ratelimit)

SMTPHandler Example
~~~~~~~~~~~~~~~~~~~

A typical use case may be to throttle error notification emails sent by
the ``logging.handlers.SMTPHandler``.

Here's an example of how you might set that up:

.. code:: python

    import logging.handlers
    import time

    from ratelimitingfilter import RateLimitingFilter

    logger = logging.getLogger('throttled_smtp_example')

    # Create an SMTPHandler
    smtp = logging.handlers.SMTPHandler(
        mailhost='smtp.example.com',
        fromaddr='from@example.com',
        toaddrs='to@example.com',
        subject='An error has occurred'
    )
    smtp.setLevel(logging.ERROR)

    # Create a formatter and set it on the handler
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    smtp.setFormatter(formatter)

    # Create an instance of the RateLimitingFilter, and add it to the handler
    ratelimit = RateLimitingFilter()
    smtp.addFilter(ratelimit)

    # Add the handler to the logger
    logger.addHandler(smtp)

    # Logged errors will now be restricted to 1 every 30 seconds
    while True:
        logger.error('An error message')
        time.sleep(2)

Advanced Usage
--------------

It is possible to pass some additional configuration options to the
``RateLimitingFilter`` initializer for further control over message
throttling.

Perhaps you want to selectively throttle particular error messages
whilst allowing other messages to pass through freely. This might be the
case if there is part of the application which you know can generate
large volumes of errors, whilst the rest of the application is unlikely
to.

One way to achieve this might be to use separate loggers, one configured
with rate limiting, one without, for the different parts of the
application. Alternatively, you can use a single logger and configure
the ``RateLimitingFilter`` to match only those messages that you want to
throttle.

Applying selective rate limiting allows for constant visbility of lower
volume errors whilst keeping the higher volume errors in check.

The ``RateLimitingFilter`` supports two ways to selectively throttle
messages:

Substring based message throttling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can pass a list of substrings to the ``RateLimitingFilter`` which it
will use to match messages to apply to.

.. code:: python

    config = {'match': ['some error', 'a different error']}

    ratelimit = RateLimitingFilter(rate=1, per=60, burst=1, **config)
    smtp.addFilter(ratelimit)

    # Can be rate limited
    logger.error('some error occurred')

    # Can be rate limited
    logger.error('a different error occurred')

    # Will not be rate limited
    logger.error('something completely different happened')

Automatic message throttling
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

*This is an experimental feature*.

You can let the ``RateLimitingFilter`` automatically throttle messages
by setting the ``match`` option to ``auto``.

.. code:: python

    config = {'match': 'auto'}
    ratelimit = RateLimitingFilter(rate=1, per=60, burst=1, **config)

The filter will then attempt to identify messages based on their content
in order to figure out whether to throttle them or not. It will tolerate
slight differences in content when identifying messages. So for example,
if error messages are being rapidly logged that are the same apart from
a timestamp, or perhaps an incrementing id, then these messages will be
treated as the same as far as rate limiting is concerned.

License
-------

MIT

Contributing
------------

Feedback and improvements are more than welcome. Please submit a pull
request!

https://github.com/wkeeling/ratelimitingfilter
