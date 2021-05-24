"""
Nose tests for acp_times.py

We cannot test for randomness here (no effective oracle),
but we can test that the elements in the returned arrow
are correct.
"""

from acp_times import open_time, close_time

import nose    # Testing framework
import arrow
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)


def test_200km():
    # Test when the control distance is within the first 60km
    assert open_time(0, 200, arrow.get("2021-01-01T00:00")) == arrow.get("2021-01-01T00:00")
    assert close_time(0, 200, arrow.get("2021-01-01T00:00")) == arrow.get("2021-01-01T01:00")

    # Testing for over night
    assert open_time(100, 200, arrow.get("2021-12-31T21:00")) == arrow.get("2021-12-31T23:56")
    assert close_time(100, 200, arrow.get("2021-12-31T21:00")) == arrow.get("2022-01-01T03:40")

    
    # When controle distacne and brevet distance are same
    assert open_time(200, 200, arrow.get("2021-05-23T12:30")) == arrow.get("2021-05-23T18:22")
    assert close_time(200, 200, arrow.get("2021-05-23T12:30")) == arrow.get("2021-05-24T02:00")

    # control distance is larger than brevet distance, but not exceeding 20% longer.
    assert open_time(205, 200, arrow.get("2021-05-23T12:30")) == arrow.get("2021-05-23T18:32")
    assert close_time(205, 200, arrow.get("2021-05-23T12:30")) == arrow.get("2021-05-24T02:00")
