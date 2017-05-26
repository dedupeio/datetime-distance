from __future__ import division

import math
from datetime import datetime
from string import ascii_lowercase

import numpy as np
from dateutil.parser import parse


class DateTimeComparator(object):

    def __init__(self, fuzzy=True, dayfirst=False, yearfirst=False):

        # kwargs for date parsing
        self.fuzzy = fuzzy  # Fuzzy match strings
        self.dayfirst = dayfirst  # Ambiguous dates are parsed dd/mm/yy
        self.yearfirst = yearfirst  # Ambiguous dates are parsed yy/mm/dd
        # Default is month-first

    def __call__(self, field_1, field_2):

        a = parse(field_1,
                  fuzzy=self.fuzzy,
                  dayfirst=self.dayfirst,
                  yearfirst=self.yearfirst)

        b = parse(field_2,
                  fuzzy=self.fuzzy,
                  dayfirst=self.dayfirst,
                  yearfirst=self.yearfirst)

        if a == b:

            # This one's easy!
            diff = 0

            # Figure out the resolution of the inputs
            resolution = self._get_resolution(a, b, field_1, field_2)

            return self._format_output(diff, resolution)

        else:

            # Negative timedeltas behave strangely, so we'll implement abs()
            # (c.f. https://docs.python.org/3/library/datetime.html#datetime.timedelta)
            if a > b:
                greater, lesser = a, b
            elif b > a:
                greater, lesser = b, a

            delta = greater - lesser

            # Determine resolution of the output
            resolution = self._get_resolution(a, b, field_1, field_2)

            if resolution == 'years':

                diff = math.log10(greater.year - lesser.year)

            elif resolution == 'months':

                # Calculate # months given # days (which datetime stores)
                yearly_delta = greater.year - lesser.year
                monthly_delta = greater.month - lesser.month

                if monthly_delta < 0:
                    monthly_delta = greater.month + (12 - lesser.month)
                    yearly_delta += 1

                total_months = (12 * yearly_delta) + monthly_delta

                diff = math.log10(total_months)

            elif resolution == 'days':

                diff = math.log10(delta.days)

            elif resolution == 'seconds':

                diff = math.log10(delta.total_seconds())

        return self._format_output(diff, resolution)

    def _get_resolution(self, a, b, field_1, field_2):

        today = datetime.today()

        # Seconds are simple: if the datetime object
        # stores them, that's the highest resolution
        if a.second > 0 and b.second > 0:
            resolution = 'seconds'

        # We'll have to be a little more clever to deal with days/months/years,
        # since dateutil's parser will default to today's day/month if either
        # of those attributes are missing
        elif a.day != today.day and b.day != today.day:
            resolution = 'days'

        else:

            f1, f2 = field_1.replace(' ', ''), field_2.replace(' ', '')

            # Assume year fields can't be longer than 4 chars ('2017')
            if ((a.month == today.month and len(f1) <= 4) or
                (b.month == today.month and len(f2) <= 4)):

                resolution = 'years'

            # Use a separate method for figuring out months
            elif ((a.day == today.day and self._is_month(field_1)) or
                  (b.day == today.day and self._is_month(field_2))):

                resolution = 'months'

            else:

                resolution = 'days'

        return resolution

    def _is_month(self, a):

        # Assume month fields must contain either alphabet characters or
        # only one hyphen, slash, or dot ('5/2017', '5.2017', '5-2017',
        # or 'May 2017')
        separators = ('.', ',', '/')

        return (any([ltr in a.lower() for ltr in list(ascii_lowercase)]) or
                len(a.split(s)) > 2 for s in separators)

    def _format_output(self, diff, resolution):

        # Map output indeces to make code more readiable
        res_map = {'seconds': 0,
                   'days':    1,
                   'months':  2,
                   'years':   3}

        # Format output template with the right resolution and delta
        output = [np.nan, np.nan, np.nan, np.nan]
        output[res_map[resolution]] = diff

        return tuple(output)
