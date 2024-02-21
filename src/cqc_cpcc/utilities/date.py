import datetime as DT

import dateparser


def format_year(year: str) -> str:
    """Formats a 4 digit year to a 2 digit year.

    Args:
    year: A 4 digit year.

    Returns:
    A 2 digit year.
    """

    year = int(year)

    if year < 100:
        y = year
    else:
        y = year % 100

    return str(y)


def get_datetime(text: str) -> DT.datetime:
    dt = dateparser.parse(text)
    if dt is None:
        raise ValueError("invalid datetime as string: " + text)
    return dt
