"""Module to create, query and update a Mongodb.

API
---
.. autoclass:: DatabaseConfig
.. autofunction:: connect_to_db

"""

__all__ = ["USERS_COLLECTION", "DatabaseConfig", "connect_to_db"]


import logging
from pathlib import Path
from typing import Dict, List, NamedTuple, Optional

import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

USERS_COLLECTION = "authenticated_users"

logger = logging.getLogger(__name__)


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""
    db_name: str
    host: Optional[str] = "localhost"
    port: Optional[int] = 27017
    username: Optional[str] = None
    password: Optional[str] = None


def connect_to_db(db_config: DatabaseConfig) -> Database:
    """Connect to a mongodb using `db_config`.

    Parameters
    ----------
    db_config
        NamedTuple with the configuration to connect to the database

    Returns
    -------
        Database

    """
    client = MongoClient(
        host=db_config.host, port=db_config.port,
        username=db_config.username, password=db_config.password)

    return client[db_config.db_name]


def store_dataframe_in_mongo(
        collection: Collection, path_csv: Path) -> List[int]:
    """Store a pandas dataframe in the database specified in `db_config`.

    Parameters
    ----------
    collection_name
        Collection name
    path_df
        Path to the csv file containing the data

    Returns
    -------
    List of the inserted objects indices

    """
    data = pd.read_csv(path_csv, index_col=0)
    data.reset_index(inplace=True)
    data.rename(columns={"index": "_id"}, inplace=True)

    return collection.insert_many(data.to_dict("records")).inserted_ids


def read_users(users_file: Path) -> List[Dict[str, str]]:
    """Read the users in the file."""
    with open(users_file, 'r') as handler:
        xs = handler.read()

    # Generate username dictionary
    users = xs.split()
    logger.info(f"Adding users to database:\n{users}")
    return [{"username": u} for u in users]


def add_users_to_db(database: Database, users_file: Path) -> None:
    """Add the allow users to the database."""
    col = database[USERS_COLLECTION]
    all_users = read_users(users_file)
    for user in all_users:
        if col.find_one(user) is None:
            col.insert_one(user)
