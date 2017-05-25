from __future__ import division

import math
from datetime import datetime, timedelta

import numpy

from dateutil.parser import parse


class DateTimeComparator(object):

    def __init__(self, fuzzy, dayfirst, yearfirst):
        pass

    def __call__(self, field_1, field_2):

        a, b = parse(field_1), parse(field_2)

        if a == b:

            return (0, 0, 0, 0)

        else:
            # Negative timedeltas behave strangely, so we'll implement abs()
            # (c.f. https://docs.python.org/3/library/datetime.html#datetime.timedelta)
            if a > b:
                delta = a - b
            elif b > a:
                delta = b - a

            # Determine resolution of the deltas
            resultion = ''
            if delta.microseconds > 0 or delta.seconds > 0:
                # Both of these resolutions should return logseconds
                diff = math.log10(delta.total_seconds())
                resolution = 'seconds'

            elif delta.days > 0:

                yearly_delta = datetime(a.year, 12, 1) - datetime(b.year, 12, 1)
                monthly_delta = datetime(a.year, a.month, 1) - datetime(b.year, b.month, 1)

                # Year is the highest resolution
                if delta.days == yearly_delta.days:
                    diff = math.log10(delta.days)
                    resolution = 'years'

                # Month is the highest resolution
                elif delta.days == monthly_delta.days:
                    diff = math.log10(delta.months)
                    resolution = 'months'

                # Just use days
                else:
                    diff = math.log10(delta.days)
                    resolution = 'days'

        # Map output indeces to make code more readiable
        output_map = {'seconds': 0,
                      'days':    1,
                      'months':  2,
                      'years':   3}

        # Update output template with the right resolution delta
        output = [np.nan, np.nan, np.nan, np.nan]
        output[output_map[resolution]] = diff

        return tuple(output)
