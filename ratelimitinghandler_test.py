import os
import time
from unittest.case import TestCase
from unittest.mock import Mock

from ratelimitinghandler import RateLimitingHandler


class RateLimitingHandlerTest(TestCase):

    def test_should_limit_to_one_record_per_second(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=1, per=1, burst=1)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 2)

    def test_should_limit_to_one_record_per_second_allowing_initial_burst_of_three(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=1, per=1, burst=3)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 4)

    def test_should_limit_to_one_record_per_two_seconds(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=1, per=2, burst=1)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 1)

    def test_should_limit_to_two_records_per_second(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=2, per=1, burst=1)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 4)

    def test_should_limit_to_two_records_per_two_seconds(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=2, per=2, burst=1)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 2)

    def test_should_limit_to_two_records_per_two_seconds_with_initial_burst_of_three(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=2, per=2, burst=3)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 4)

    def test_should_limit_to_no_records_per_second(self):
        mock_target = Mock()
        handler = RateLimitingHandler(mock_target, rate=0, per=0, burst=0)

        self._emit_twenty_records_over_two_seconds(handler)

        self.assertEqual(mock_target.emit.call_count, 0)

    def _emit_twenty_records_over_two_seconds(self, handler):
        mock_record = Mock()

        for _ in range(20):
            handler.emit(mock_record)
            time.sleep(0.1)

    def test_should_append_num_limited_records_to_message(self):
        emitted = []
        mock_target = Mock()
        mock_target.emit.side_effect = lambda rec: emitted.append(rec)
        handler = RateLimitingHandler(mock_target, rate=1, per=1, burst=4)

        for _ in range(30):
            mock_record = Mock()
            mock_record.msg = 'test message'
            handler.emit(mock_record)
            time.sleep(0.1)

        self.assertEqual(len(emitted), 6)
        self.assertTrue(emitted[4].msg.endswith(os.linesep + '... 6 additional messages suppressed'))
        self.assertTrue(emitted[5].msg.endswith(os.linesep + '... 9 additional messages suppressed'))
