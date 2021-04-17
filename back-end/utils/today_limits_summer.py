from datetime import datetime


def today_datetime():
    """ This function returns the datetime limits of the current UTC date
        @returns
            today_start:    (datetime)  the first moment of current day
            today_end:      (datetime)  the last moment of current day
    """

    str_now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    now = datetime.strptime(str_now, '%Y-%m-%d %H:%M:%S').timetuple()
    today_start = datetime(now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0)
    today_end = datetime(now.tm_year, now.tm_mon, now.tm_mday, 23, 59, 59)

    return today_start, today_end
