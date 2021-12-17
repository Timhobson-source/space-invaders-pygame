import unittest

from src.helpers import clip_value


class TestClipValue(unittest.TestCase):
    def test_value_between_min_max(self):
        self.assertEqual(clip_value(4, 3, 5), 4)

    def test_value_below_minimum(self):
        self.assertEqual(clip_value(1, 3, 5), 3)

    def test_value_above_maximum(self):
        self.assertEqual(clip_value(7, 3, 5), 5)

    def test_value_equals_minimum(self):
        self.assertEqual(clip_value(3, 3, 5), 3)

    def test_value_equals_maximum(self):
        self.assertEqual(clip_value(5, 3, 5), 5)
