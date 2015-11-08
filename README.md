RateLimitingFilter
==================
The RateLimitingFilter is a filter for the Python logging system that allows you to restrict the flow of messages sent through your logging handlers based upon how quickly they arrive.

The filter can be useful if you're using a handler such as Python's `logging.handlers.SMTPHandler` to send error notification emails. Error notification emails provide a useful means of keeping an eye on the health of a running system, but these emails have the potential to overload a mailbox if they start arriving in quick succession due to some kind of critical failure.

This filter can help prevent mailbox overload by throttling messages based on a configurable rate, whilst allowing for initial bursts of messages which can be a useful indicator that something somewhere has broken.

Basic Usage
-----------
As mentioned, a typical use case may be to throttle error notification emails sent by the `logging.handlers.SMTPHandler`. 

Create an instance of the `RateLimitingFilter`. Supplying no arguments defaults to a flow rate of 1 message every 30 seconds. 

```
f = RateLimitingFilter()
```

You can customise the flow rate by supplying your own values for the `rate`, `per` and `burst` attributes. For example, to allow a rate of 3 messages per minute with a periodic burst of up to 10 messages:

```
f = RateLimitingFilter(rate=3, per=60, burst=10)
```

Then it is just a case of adding the filter to your handler.

```


Advanced Usage
--------------

License
--------

Contributing
-------------



