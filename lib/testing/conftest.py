#!/usr/bin/env python3

import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["SQLALCHEMY_SILENCE_UBER_WARNING"] = "1"

package_dir = "/".join(os.path.abspath(os.path.dirname(__file__)).split("/")[0:-1])
db_dir = os.path.join(package_dir, "one_to_many.db")
SQLITE_URL = "".join(["sqlite:///", db_dir])


@pytest.fixture(scope="session")
def session():
    engine = create_engine(SQLITE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.close()


def pytest_itemcollected(item):
    par = item.parent.obj
    node = item.obj
    pref = par.__doc__.strip() if par.__doc__ else par.__class__.__name__
    suf = node.__doc__.strip() if node.__doc__ else node.__name__
    if pref or suf:
        item._nodeid = " ".join((pref, suf))
