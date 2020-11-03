"""Module to create, query and update a Mongodb.

API
---
.. autoclass:: DatabaseConfig
.. autofunction:: connect_to_db

"""

__all__ = ["DatabaseConfig", "connect_to_db"]


from pathlib import Path
from typing import List, NamedTuple, Optional

import pandas as pd
from pymongo import MongoClient
from pymongo.collection import Collection


class DatabaseConfig(NamedTuple):
    """Data to store the database configuration."""
    db_name: str
    host: Optional[str] = "localhost"
    port: Optional[int] = 27017
    username: Optional[str] = None
    password: Optional[str] = None


def connect_to_db(db_config: DatabaseConfig) -> MongoClient:
    """Connect to a mongodb using `db_config`.

    Parameters
    ----------
    db_config
        NamedTuple with the configuration to connect to the database

    Returns
    -------
        MongoClient

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
