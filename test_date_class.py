"""Automated tests for the Date wrapper class."""

import unittest
from date_class import Date


class TestDate(unittest.TestCase):
    """Check construction, read-only properties, updates, calendar rules, and formats."""

    def test_default_constructor(self):
        value = Date()
        self.assertEqual((value.month, value.day, value.year), (1, 1, 1900))

    def test_valid_constructor(self):
        value = Date(12, 25, 2021)
        self.assertEqual((value.month, value.day, value.year), (12, 25, 2021))

    def test_valid_leap_day(self):
        self.assertEqual(Date(2, 29, 2024).day, 29)

    def test_year_boundaries(self):
        self.assertEqual(Date(1, 1, 1).year, 1)
        self.assertEqual(Date(12, 31, 9999).year, 9999)

    def test_invalid_constructor_dates(self):
        for month, day, year in [(0, 1, 2024), (13, 1, 2024), (4, 31, 2024),
                                 (2, 29, 2023), (1, 0, 2024), (1, 32, 2024),
                                 (1, 1, 0), (1, 1, 10000)]:
            with self.subTest(month=month, day=day, year=year):
                with self.assertRaises(ValueError):
                    Date(month, day, year)

    def test_properties_are_read_only(self):
        value = Date()
        for property_name in ("month", "day", "year"):
            with self.subTest(property_name=property_name):
                with self.assertRaises(AttributeError):
                    setattr(value, property_name, 5)

    def test_set_date_valid(self):
        value = Date()
        self.assertIsNone(value.set_date(2, 29, 2024))
        self.assertEqual((value.month, value.day, value.year), (2, 29, 2024))

    def test_set_date_invalid_preserves_original(self):
        value = Date(12, 25, 2021)
        for invalid in [(2, 29, 2021), (13, 1, 2024), (4, 31, 2024)]:
            with self.subTest(invalid=invalid):
                with self.assertRaises(ValueError):
                    value.set_date(*invalid)
                self.assertEqual((value.month, value.day, value.year), (12, 25, 2021))

    def test_instance_leap_year(self):
        for year, expected in [(2024, True), (2023, False), (2000, True), (1900, False)]:
            with self.subTest(year=year):
                self.assertIs(Date(1, 1, year).is_leap_year(), expected)

    def test_static_leap_year(self):
        for year, expected in [(2024, True), (2023, False), (2000, True), (1900, False)]:
            with self.subTest(year=year):
                self.assertIs(Date.is_year_leap(year), expected)

    def test_instance_last_day(self):
        for month, year, expected in [(2, 2024, 29), (2, 2023, 28),
                                      (4, 2024, 30), (12, 2024, 31)]:
            with self.subTest(month=month, year=year):
                self.assertEqual(Date(month, 1, year).last_day(), expected)

    def test_static_last_day(self):
        for month, year, expected in [(2, 2024, 29), (2, 2023, 28),
                                      (4, 2024, 30), (12, 2024, 31)]:
            with self.subTest(month=month, year=year):
                self.assertEqual(Date.last_day_of_month(month, year), expected)

    def test_static_last_day_invalid_month(self):
        for month in (0, 13):
            with self.subTest(month=month):
                with self.assertRaises(ValueError):
                    Date.last_day_of_month(month, 2024)

    def test_numeric_format(self):
        self.assertEqual(Date(12, 25, 2021).to_numeric_string(), "12/25/2021")

    def test_month_first_format(self):
        self.assertEqual(Date(12, 25, 2021).to_month_first_string(), "December 25, 2021")

    def test_day_first_format(self):
        self.assertEqual(Date(12, 25, 2021).to_day_first_string(), "25 December 2021")

    def test_format_zero_padding(self):
        value = Date(1, 2, 2024)
        self.assertEqual(value.to_numeric_string(), "01/02/2024")
        self.assertEqual(value.to_month_first_string(), "January 02, 2024")
        self.assertEqual(value.to_day_first_string(), "02 January 2024")

    def test_formats_update_after_set_date(self):
        value = Date()
        value.set_date(12, 25, 2021)
        self.assertEqual(value.to_numeric_string(), "12/25/2021")

    def test_subtract_dates_positive(self):
        """Test subtracting an earlier date from a later date."""
        later = Date(1, 10, 2024)
        earlier = Date(1, 5, 2024)
        self.assertEqual(later - earlier, 5)

    def test_subtract_dates_negative(self):
        """Test subtraction when the second date is later."""
        earlier = Date(1, 5, 2024)
        later = Date(1, 10, 2024)
        self.assertEqual(earlier - later, -5)

    def test_subtract_same_date(self):
        """Test that subtracting identical dates returns zero."""
        first = Date(6, 15, 2024)
        second = Date(6, 15, 2024)
        self.assertEqual(first - second, 0)

    def test_subtract_across_leap_day(self):
        """Test subtraction across February 29 in a leap year."""
        before = Date(2, 28, 2024)
        after = Date(3, 1, 2024)
        self.assertEqual(after - before, 2)

    def test_increment(self):
        """Test moving a date forward by one day."""
        value = Date(5, 15, 2024)
        result = value.increment()
        self.assertEqual(value.to_numeric_string(), "05/16/2024")
        self.assertIs(result, value)

    def test_increment_end_of_month(self):
        """Test incrementing across a month boundary."""
        value = Date(4, 30, 2024)
        value.increment()
        self.assertEqual(value.to_numeric_string(), "05/01/2024")

    def test_increment_end_of_year(self):
        """Test incrementing across a year boundary."""
        value = Date(12, 31, 2024)
        value.increment()
        self.assertEqual(value.to_numeric_string(), "01/01/2025")

    def test_increment_leap_day(self):
        """Test incrementing onto February 29 during a leap year."""
        value = Date(2, 28, 2024)
        value.increment()
        self.assertEqual(value.to_numeric_string(), "02/29/2024")

    def test_decrement(self):
        """Test moving a date backward by one day."""
        value = Date(5, 15, 2024)
        result = value.decrement()
        self.assertEqual(value.to_numeric_string(), "05/14/2024")
        self.assertIs(result, value)

    def test_decrement_start_of_month(self):
        """Test decrementing across a month boundary."""
        value = Date(5, 1, 2024)
        value.decrement()
        self.assertEqual(value.to_numeric_string(), "04/30/2024")

    def test_decrement_start_of_year(self):
        """Test decrementing across a year boundary."""
        value = Date(1, 1, 2025)
        value.decrement()
        self.assertEqual(value.to_numeric_string(), "12/31/2024")

    def test_decrement_leap_day(self):
        """Test decrementing onto February 29 during a leap year."""
        value = Date(3, 1, 2024)
        value.decrement()
        self.assertEqual(value.to_numeric_string(), "02/29/2024")


if __name__ == "__main__":
    unittest.main()
