"""Module to test the interface to Mongodb."""


from typing import List

from pymongo import MongoClient
from pymongo.database import Database

from insilicoserver.mongo_interface import (DatabaseConfig, connect_to_db,
                                            store_dataframe_in_mongo)
from insilicoserver.query_resolvers import get_jobs_by_size

from .utils_test import PATH_TEST, read_jobs

DB_NAME = "test_mutations"
COLLECTION_NAME = "candidates"


def add_candidates(mongodb: MongoClient) -> List[int]:
    """Check that the interface is working."""
    # read data from file
    path_data = PATH_TEST / "candidates.csv"

    return store_dataframe_in_mongo(mongodb[COLLECTION_NAME], path_data)


def get_database() -> Database:
    """Return client to MongoDB."""
    db_config = DatabaseConfig(DB_NAME)
    return connect_to_db(db_config)


def test_many_insertions():
    """Check that the interface is working."""
    # Connect to the database
    mongodb = get_database()

    expected_ids = {76950, 43380, 26717, 70, 47561, 32800, 37021, 2449, 63555, 72987}
    try:
        ids = add_candidates(mongodb)
        print("received ids: ", ids)
        assert all(index in expected_ids for index in ids)
    finally:
        collection = mongodb[COLLECTION_NAME]
        collection.drop()


def test_aggregation():
    """Test an aggregation pipeline."""
    mongodb = get_database()
    col = mongodb["jobs_test"]
    jobs = read_jobs()
    col.insert_many(jobs)
    try:
        large = next(get_jobs_by_size("LARGE", col))
        assert large["_id"] == 135037
    finally:
        col.drop()
