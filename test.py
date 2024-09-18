from datetime import datetime
from collect_assignments import calculate_late_days
import unittest

class TestLateDays(unittest.TestCase):

    def test_foo(self):
        cases = [
            ((datetime(2020, 10, 29, 2, 0), datetime(2020, 10, 25)), 0),
            ((datetime(2020, 10, 29, 2, 0), datetime(2020, 10, 28)), 0),
            ((datetime(2020, 10, 29, 2, 0), datetime(2020, 10, 29, 1)), 0),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 29)), 0),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 29, 23, 59)), 0),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 30)), 1),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 30, 2, 59)), 1),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 30, 23, 59)), 1),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 10, 31, 23, 59)), 2),
            ((datetime(2020, 10, 29, 23, 59), datetime(2020, 11, 1, 23, 59)), 3),
            ]
        for i, case in enumerate(cases):
            with self.subTest(i=f"case_index:{i}"):
                (deadline, submitted), expected = case
                self.assertEqual(calculate_late_days(deadline, submitted),  expected)


if __name__ == "__main__":
    unittest.main()
