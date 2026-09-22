"""A validated calendar-date wrapper built using the Python standard library."""

from datetime import date
import calendar


class Date:
    """Represent a valid calendar date using one private datetime.date object.

    Invalid constructor dates raise ValueError. The month, day, and year
    are exposed as read-only properties.
    """

    def __init__(self, month: int = 1, day: int = 1, year: int = 1900) -> None:
        """Create a date from month, day, and year; raise ValueError if invalid."""
        self.__date = date(year, month, day)

    @property
    def month(self) -> int:
        """Return the stored month as an integer from 1 through 12."""
        return self.__date.month

    @property
    def day(self) -> int:
        """Return the stored day of the month as an integer."""
        return self.__date.day

    @property
    def year(self) -> int:
        """Return the stored year as an integer."""
        return self.__date.year

    def set_date(self, month: int, day: int, year: int) -> None:
        """Replace the whole date; raise ValueError and retain the old date if invalid."""
        new_date = date(year, month, day)
        self.__date = new_date

    def is_leap_year(self) -> bool:
        """Return whether the stored year is a leap year."""
        return calendar.isleap(self.year)

    @staticmethod
    def is_year_leap(year: int) -> bool:
        """Return whether the supplied year is a leap year."""
        return calendar.isleap(year)

    def last_day(self) -> int:
        """Return the last valid day number in the stored month."""
        return calendar.monthrange(self.year, self.month)[1]

    @staticmethod
    def last_day_of_month(month: int, year: int) -> int:
        """Return the last day of the supplied month and year; invalid months raise calendar.IllegalMonthError (a ValueError)."""
        return calendar.monthrange(year, month)[1]

    def to_numeric_string(self) -> str:
        """Return the date in MM/DD/YYYY format, such as 12/25/2021."""
        return self.__date.strftime("%m/%d/%Y")

    def to_month_first_string(self) -> str:
        """Return the date as Month DD, YYYY, such as December 25, 2021."""
        return self.__date.strftime("%B %d, %Y")

    def to_day_first_string(self) -> str:
        """Return the date as DD Month YYYY, such as 25 December 2021."""
        return self.__date.strftime("%d %B %Y")
