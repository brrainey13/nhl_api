"""
Utility functions for the NHL API Wrapper.
"""

import datetime
import typing as t


def format_date(date: t.Union[str, datetime.date]) -> str:
    """
    Ensures a date is in YYYY-MM-DD format.

    Args:
        date: A string or datetime.date object.

    Returns:
        Date string in YYYY-MM-DD format.

    Raises:
        ValueError: If the input format is invalid.
    """
    if isinstance(date, datetime.date):
        return date.strftime("%Y-%m-%d")
    elif isinstance(date, str):
        # Basic validation, could be more robust
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            raise ValueError("Date string must be in YYYY-MM-DD format")
    else:
        raise TypeError("Date must be a string or datetime.date object")


# Add other helpers as needed, e.g., for building cayenneExp strings for the stats API later.
