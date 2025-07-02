import unittest
from logging import LogRecord
from filters import LevelFilter, RangeFilter, AnyFilter

class DummyLogRecord(LogRecord):
    def __init__(self, levelno, msg="", name="test", pathname="", lineno=0):
        super().__init__(name, levelno, pathname, lineno, msg, args=(), exc_info=None)

class TestLevelFilter(unittest.TestCase):
    def test_level_match(self):
        filt = LevelFilter(20)
        record = DummyLogRecord(20)
        self.assertTrue(filt.filter(record))

    def test_level_no_match(self):
        filt = LevelFilter(30)
        record = DummyLogRecord(20)
        self.assertFalse(filt.filter(record))

class TestRangeFilter(unittest.TestCase):
    def test_in_range(self):
        filt = RangeFilter(10, 30)
        record = DummyLogRecord(20)
        self.assertTrue(filt.filter(record))

    def test_below_range(self):
        filt = RangeFilter(10, 30)
        record = DummyLogRecord(5)
        self.assertFalse(filt.filter(record))

    def test_above_range(self):
        filt = RangeFilter(10, 30)
        record = DummyLogRecord(40)
        self.assertFalse(filt.filter(record))

    def test_min_max_swapped(self):
        filt = RangeFilter(30, 10)
        record = DummyLogRecord(20)
        self.assertTrue(filt.filter(record))

class TestAnyFilter(unittest.TestCase):
    def test_any_filter_true(self):
        f1 = LevelFilter(10)
        f2 = LevelFilter(20)
        anyf = AnyFilter(f1, f2)
        record = DummyLogRecord(20)
        self.assertTrue(anyf.filter(record))

    def test_any_filter_false(self):
        f1 = LevelFilter(10)
        f2 = LevelFilter(30)
        anyf = AnyFilter(f1, f2)
        record = DummyLogRecord(20)
        self.assertFalse(anyf.filter(record))

    def test_any_filter_empty(self):
        anyf = AnyFilter()
        record = DummyLogRecord(20)
        self.assertFalse(anyf.filter(record))

if __name__ == "__main__":
    unittest.main()
