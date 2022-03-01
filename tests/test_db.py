import pytest
from database.db import Database
from database.connection import Connection


def test_storage():
    """ Asserts that a value can be stored and retrieved from your database """
    test_connection = Connection.get_db_connection()
    d = Database()
    k, v = "A", 1
    d.set(k, v, test_connection)
    assert v == d.get(k, test_connection)[0]


def test_keys():
    """ Asserts that a keys() call to your database returns a key set """
    test_connection = Connection.get_db_connection()
    d = Database()
    data = {"1": 1,
            "FOMO": 1,
            "TOMO": 1}

    assert list(data.keys()) == d.keys(test_connection)

