import logging
import os
from unittest.case import TestCase
from mock import Mock, patch

from ratelimitingfilter import RateLimitingFilter


class RateLimitingFilterTest(TestCase):
    def setUp(self):
        patcher = patch('ratelimitingfilter.ratelimitingfilter.time')
        self.mock_time = patcher.start()
        self.addCleanup(patcher.stop)
        self.mock_time.return_value = 0

    def test_limit_to_one_record_per_second(self):
        f = RateLimitingFilter(rate=1, per=1, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 2)

    def test_limit_to_one_record_per_second_allowing_initial_burst_of_three(self):
        f = RateLimitingFilter(rate=1, per=1, burst=3)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_limit_to_one_record_per_two_seconds(self):
        f = RateLimitingFilter(rate=1, per=2, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 1)

    def test_limit_to_two_records_per_second(self):
        f = RateLimitingFilter(rate=2, per=1, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_limit_to_two_records_per_two_seconds(self):
        f = RateLimitingFilter(rate=2, per=2, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 2)

    def test_limit_to_two_records_per_two_seconds_with_initial_burst_of_three(self):
        f = RateLimitingFilter(rate=2, per=2, burst=3)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_limit_to_no_records_per_second(self):
        f = RateLimitingFilter(rate=0, per=0, burst=0)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 0)

    def _filter_twenty_records_over_two_seconds(self, f):
        mock_record = Mock()
        mock_record.msg = 'test message'

        result = []

        for _ in range(20):
            result.append(f.filter(mock_record))
            self.mock_time.return_value += 0.1

        return result

    def test_append_num_limited_records_to_message(self):
        filtered = []
        f = RateLimitingFilter(rate=1, per=1, burst=4)

        for _ in range(30):
            mock_record = Mock()
            mock_record.msg = 'test message'
            if f.filter(mock_record):
                filtered.append(mock_record)
            self.mock_time.return_value += 0.1

        self.assertEqual(len(filtered), 6)
        self.assertTrue(filtered[4].msg.endswith(os.linesep + '... 6 additional messages suppressed'))
        self.assertTrue(filtered[5].msg.endswith(os.linesep + '... 9 additional messages suppressed'))

    def test_rate_limit_messages_matching_substring(self):
        config = {'match': ['rate limited']}
        f = RateLimitingFilter(rate=1, per=1, burst=1, **config)

        mock_matching_record = Mock()
        mock_matching_record.msg = 'a rate limited test message'

        mock_non_matching_record = Mock()
        mock_non_matching_record.msg = 'a different test message'

        result = []

        for _ in range(20):
            if f.filter(mock_matching_record):
                result.append(mock_matching_record.msg)  # Only 2 of these get logged as they match the substring
            if f.filter(mock_non_matching_record):
                result.append(mock_non_matching_record.msg)  # 20 of these get logged as they don't match
            self.mock_time.return_value += 0.1

        self.assertEqual(len([m for m in result if 'a rate limited test message' in m]), 2)
        self.assertEqual(result.count('a different test message'), 20)

    def test_rate_limit_messages_automatically(self):
        config = {'match': 'auto'}
        f = RateLimitingFilter(rate=1, per=1, burst=1, **config)

        result = []

        for i in range(20):
            mock_varying_record = Mock()
            mock_varying_record.msg = 'a rate limited varying message: {varying}'.format(varying=i)

            mock_rate_limited_record = Mock()
            mock_rate_limited_record.msg = 'a completely different message'

            if f.filter(mock_varying_record):
                # Only 2 of these get logged as they are considered the same message,
                # even though they are not identical
                result.append(mock_varying_record.msg)
            if f.filter(mock_rate_limited_record):
                # Only 2 of these get logged as they are the all identical
                result.append(mock_rate_limited_record.msg)
            self.mock_time.return_value += 0.1

        self.assertEqual(len([m for m in result if 'a rate limited varying message' in m]), 2)
        self.assertEqual(len([m for m in result if 'a completely different message' in m]), 2)

    def test_log_exception(self):
        logger = logging.getLogger('test')
        handler = logging.StreamHandler()
        throttle = RateLimitingFilter(rate=1, per=1, burst=1)
        handler.addFilter(throttle)
        logger.addHandler(handler)

        try:
            logger.error('First')
            raise RuntimeError('Expected exception')
        except RuntimeError as e:
            logger.exception(e)  # Should be throttled
