from __future__ import division

import math
from collections import namedtuple

from dateutil.parser import parse
import dateutil.parser as parser


# Monkey patch the parser module to get resolution
def resolution(self, timestr, default=None,
               ignoretz=False, tzinfos=None,
               **kwargs):
    return self._parse(timestr, **kwargs)

parser.parser.resolution = resolution


class DateTimeComparator(object):

    def __init__(self, fuzzy=True, dayfirst=False, yearfirst=False):

        # kwargs for date parsing
        self.fuzzy = fuzzy  # Fuzzy match strings
        self.dayfirst = dayfirst  # Ambiguous dates are parsed dd/mm/yy
        self.yearfirst = yearfirst  # Ambiguous dates are parsed yy/mm/dd
        # Default is month-first

        # Map output indeces to make code more readiable
        self.res_map = {'seconds': 0,
                        'days':    1,
                        'months':  2,
                        'years':   3}

        # Make the resolution parser a class method
        self.parse_resolution = parser.parser().resolution

    def parse_timestamp(self, field):

        return parse(field,
                     fuzzy=self.fuzzy,
                     dayfirst=self.dayfirst,
                     yearfirst=self.yearfirst)

    def __call__(self, field_1, field_2):

        a, b = self.parse_timestamp(field_1), self.parse_timestamp(field_2)

        if a == b:

            # This one's easy!
            diff = 0

            # Figure out the resolution of the inputs
            resolution = self._get_resolution(field_1, field_2)

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
            resolution = self._get_resolution(field_1, field_2)

            if resolution == 'years':

                diff = math.sqrt(greater.year - lesser.year)

            elif resolution == 'months':

                # Calculate # months given # days (which datetime stores)
                yearly_delta = greater.year - lesser.year
                monthly_delta = greater.month - lesser.month

                if monthly_delta < 0:
                    monthly_delta = greater.month + (12 - lesser.month)
                    yearly_delta += 1

                total_months = (12 * yearly_delta) + monthly_delta

                # We want the significance of each additional unit of
                # difference to decrease as the delta gets large. Hence,
                # we return the square root of the delta.
                diff = math.sqrt(total_months)

            elif resolution == 'days':

                diff = math.sqrt(delta.days)

            elif resolution == 'seconds':

                diff = math.sqrt(delta.total_seconds())

        return self._format_output(diff, resolution)

    def _get_resolution(self, field_1, field_2):

        try:
            res_a = self.parse_resolution(field_1)[0]
            assert res_a is not None
        except (TypeError, AssertionError):
            if self.fuzzy:
                # We need to handle fuzzy parses of strings differently
                a = str(self.parse_timestamp(field_1))
                res_a = self.parse_resolution(a)[0]

        try:
            res_b = self.parse_resolution(field_2)[0]
            assert res_b is not None
        except (TypeError, AssertionError):
            if self.fuzzy:
                b = str(self.parse_timestamp(field_2))
                res_b = self.parse_resolution(b)[0]

        # We have to test for NoneType here, since the parser can return
        # a falsey value of 0 in the case of 0 seconds (12:30:00)
        if res_a.second is not None and res_b.second is not None:
            resolution = 'seconds'

        elif res_a.day and res_b.day:
            resolution = 'days'

        elif res_a.month and res_b.month:
            resolution = 'months'

        else:
            resolution = 'years'

        return resolution

    def _make_tuple(self, tup):

        # Return a named tuple
        tup_names = [res + '_dummy' for res in self.res_map.keys()]
        tup_names += [res + '_derived' for res in self.res_map.keys()]
        Output = namedtuple('DateTime', tup_names)

        return Output._make(tup)

    def _format_output(self, diff, resolution):

        # Format output template with the right resolution and delta
        output = [0 for _ in range(8)]
        output[self.res_map[resolution]] = 1
        output[4 + self.res_map[resolution]] = diff

        return self._make_tuple(output)
