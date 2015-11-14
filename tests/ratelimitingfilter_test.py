import os
import time
from unittest.case import TestCase
from unittest.mock import Mock

from ratelimitingfilter import RateLimitingFilter


class RateLimitingFilterTest(TestCase):

    def test_should_limit_to_one_record_per_second(self):
        f = RateLimitingFilter(rate=1, per=1, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 2)

    def test_should_limit_to_one_record_per_second_allowing_initial_burst_of_three(self):
        f = RateLimitingFilter(rate=1, per=1, burst=3)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_should_limit_to_one_record_per_two_seconds(self):
        f = RateLimitingFilter(rate=1, per=2, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 1)

    def test_should_limit_to_two_records_per_second(self):
        f = RateLimitingFilter(rate=2, per=1, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_should_limit_to_two_records_per_two_seconds(self):
        f = RateLimitingFilter(rate=2, per=2, burst=1)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 2)

    def test_should_limit_to_two_records_per_two_seconds_with_initial_burst_of_three(self):
        f = RateLimitingFilter(rate=2, per=2, burst=3)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 4)

    def test_should_limit_to_no_records_per_second(self):
        f = RateLimitingFilter(rate=0, per=0, burst=0)

        result = self._filter_twenty_records_over_two_seconds(f)

        self.assertEqual(result.count(True), 0)

    def _filter_twenty_records_over_two_seconds(self, f):
        mock_record = Mock()
        mock_record.msg = 'test message'

        result = []

        for _ in range(20):
            result.append(f.filter(mock_record))
            time.sleep(0.1)

        return result

    def test_should_append_num_limited_records_to_message(self):
        filtered = []
        f = RateLimitingFilter(rate=1, per=1, burst=4)

        for _ in range(30):
            mock_record = Mock()
            mock_record.msg = 'test message'
            if f.filter(mock_record):
                filtered.append(mock_record)
            time.sleep(0.1)

        self.assertEqual(len(filtered), 6)
        self.assertTrue(filtered[4].msg.endswith(os.linesep + '... 6 additional messages suppressed'))
        self.assertTrue(filtered[5].msg.endswith(os.linesep + '... 9 additional messages suppressed'))
