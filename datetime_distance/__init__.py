import math
import datetime

from dateutil.parser import parse


class DateTimeComparator(object):

    def __call__(field_1, field_2):

        a, b = parse(field_1), parse(field_2)

        if a > b:
            delta = math.log10(a) - math.log10(b)
        elif b > a:
            delta = math.log10(b) - math.log10(a)
        else:
            delta = datetime.timedelta()

        return delta.total_seconds()
