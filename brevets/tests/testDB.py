"""
Nose tests for database. Especially for insertion and deletion
"""

from pymongo import MongoClient
from dbclass import Mongo

import nose
import logging

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

def test_db():
    tester = Mongo("ourdb")
    tester.connect()
    tester.set_db("testdb")

    rows = [{'km': 10, 'open': '2021-01-01T18:19', 'close': '2021-01-02T07:49'},
            {'km': 20, 'open': '2021-12-01T00:100', 'close': '2021-12-01T012:45'}]

    for row in rows:
        test_client.insert("testcollection", row)
    assert test_client.list_all_rows("testcollection") == rows

    test_client.delete_all_rows("testcollection")
    assert test_client.list_all_rows("testcollection") == []
