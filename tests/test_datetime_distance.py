import math
import unittest

import numpy as np

from datetime_distance import DateTimeComparator


class DateTimeTest(unittest.TestCase):

    def test_datetime_to_datetime_comparison(self):

        dt1 = '2017-05-25'
        dt2 = '2017-01-01'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (np.nan, math.log10(144), np.nan, np.nan)

        self.assertAlmostEqual(distance, expected)

    def test_datetime_to_timestamp_comparison(self):

        dt1 = '2017-05-25'
        dt2 = '2017-01-01 12:30:05'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (np.nan, math.log10(144), np.nan, np.nan)

        self.assertAlmostEqual(distance, expected)

    def test_timestamp_to_timestamp_comparison(self):

        dt1 = '2017-05-25 21:08:09'
        dt2 = '2017-01-01 12:30:05'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (math.log10(12472684), np.nan, np.nan, np.nan)

        self.assertAlmostEqual(distance, expected)

    def test_years(self):

        dt1 = '2012'
        dt2 = '2010'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (np.nan, np.nan, np.nan, math.log10(2))

        self.assertAlmostEqual(distance, expected)

    def test_months(self):

        dt1 = 'May 2012'
        dt2 = 'June 2013'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (np.nan, np.nan, math.log10(13), np.nan)

        self.assertAlmostEqual(distance, expected)

    def test_days(self):

        dt1 = '5 May 2013'
        dt2 = '9 June 2013'

        c = DateTimeComparator()
        distance = c(dt1, dt2)
        expected = (np.nan, math.log(35), np.nan, np.nan)

        self.assertAlmostEqual(distance, expected)

    def test_strange_formats(self):

        dt1 = 'May 5th, 2013'
        dt2 = '2013-09-06'

        dt3 = '11am May 5th 2013'
        dt4 = 'June 6th 2014'

        dt5 = '5/5/2013'
        dt6 = '6/9/2013'

        c = DateTimeComparator()

        distance1 = c(dt1, dt2)
        distance2 = c(dt3, dt4)
        distance3 = c(dt5, dt6)
        expected = (np.nan, math.log(35), np.nan, np.nan)

        self.assertAlmostEqual(distance1, expected)
        self.assertAlmostEqual(distance2, expected)
        self.assertAlmostEqual(distance3, expected)

    def test_misspellings(self):
        pass
