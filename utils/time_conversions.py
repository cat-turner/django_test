import datetime

import dateparser


def get_utc_time(datestring: str) -> datetime.datetime:
    # datetime with tzinfo
    time_str = dateparser.parse(datestring)
    # convert the time to utc timezone
    return time_str.astimezone(datetime.timezone.utc)
