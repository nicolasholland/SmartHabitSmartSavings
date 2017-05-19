import time

def epoch_to_datetime(seconds):
    """ Returns time object.

        Examples
        --------
        >>> import read_data
        >>> d = read_data.epoch_to_datetime(1379879533)
        >>> d.tm_year
        2013
        >>> d.tm_mon
        9
        >>> d.tm_mday
        22
        >>> d.tm_hour
        19
        >>> d.tm_min
        52
        >>> d.tm_sec
        13
    """
    return time.gmtime(seconds)
