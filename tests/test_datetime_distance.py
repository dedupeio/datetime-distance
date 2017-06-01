import math

import numpy as np

import env
from datetime_distance import DateTimeComparator

def test_datetime_to_datetime_comparison():

    dt1 = '2017-05-25'
    dt2 = '2017-01-01'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([0, 1, 0, 0, 0, math.sqrt(144), 0, 0])

    print(distance)
    print(expected)

    np.testing.assert_array_equal(distance, expected)

def test_datetime_to_timestamp_comparison():

    dt1 = '2017-05-25'
    dt2 = '2017-01-01 12:30:05'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([0, 1, 0, 0, 0, math.sqrt(143), 0, 0])

    np.testing.assert_array_equal(distance, expected)

def test_timestamp_to_timestamp_comparison():

    dt1 = '2017-05-25 21:08:09'
    dt2 = '2017-01-01 12:30:05'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([1, 0, 0, 0, math.sqrt(12472684), 0, 0, 0])

    np.testing.assert_array_equal(distance, expected)

def test_years():

    dt1 = '2012'
    dt2 = '2010'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([0, 0, 0, 1, 0, 0, 0, math.sqrt(2)])

    np.testing.assert_array_equal(distance, expected)

def test_months():

    dt1 = 'May 2012'
    dt2 = 'June 2013'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([0, 0, 1, 0, 0, 0, math.sqrt(13), 0])

    np.testing.assert_array_equal(distance, expected)

def test_days():

    dt1 = '5 May 2013'
    dt2 = '9 June 2013'

    c = DateTimeComparator()
    distance = c(dt1, dt2)
    expected = np.array([0, 1, 0, 0, 0, math.sqrt(35), 0, 0])

    np.testing.assert_array_equal(distance, expected)

def test_alternate_formats():

    c = DateTimeComparator()

    dt1 = 'May 5th, 2013'
    dt2 = '2013-06-09'

    distance1 = c(dt1, dt2)
    expected1 = np.array([0, 1, 0, 0, 0, math.sqrt(35), 0, 0])

    np.testing.assert_array_equal(distance1, expected1)

    dt3 = '11am May 5th 2013'
    dt4 = 'June 9th 2013'

    distance2 = c(dt3, dt4)
    expected2 = np.array([0, 1, 0, 0, 0, math.sqrt(34), 0, 0])

    np.testing.assert_array_equal(distance2, expected2)

    dt5 = '5/5/2013'
    dt6 = '6/9/2013'

    distance3 = c(dt5, dt6)
    expected3 = expected1

    np.testing.assert_array_equal(distance3, expected3)

def test_misspellings():
    pass
