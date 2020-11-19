"""Functionality to authenticate the user.

API
---
.. autofunction:: authenticate_username
.. autofunction: add_users_to_db

"""
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional

import requests
from pymongo.database import Database

__all__ = ["USERS_COLLECTION", "add_users_to_db", "authenticate_username"]

logger = logging.getLogger(__name__)

USERS_COLLECTION = "authenticated_users"


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
        col.update_one(user, user, upsert=True)


def authenticate_username(
        token: str,
        github_api: str = 'https://api.github.com/graphql') -> Optional[str]:
    """Check that the token correspond to a valid GitHub username.

    Using  `GitHub GraphQL API v4 <https://developer.github.com/v4/>`_

    Parameters
    ----------
    token
        GitHub token that gives read only authorization
    github_api
        URL of GitHub's API

    Return
    ------
    GitHub's username or None

    """
    headers = {'Authorization': f'bearer {token}'}
    query = "query { viewer { login }}"
    reply = requests.post(github_api, json={'query': query}, headers=headers)

    status = reply.status_code
    if status != 200:
        return None

    data = json.loads(reply.text)['data']
    return data['viewer']['login']
