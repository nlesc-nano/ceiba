"""Functionality to authenticate the user.

API
---
.. autofunction:: authenticate_username
.. autofunction: add_users_to_db

"""
import json
from typing import Optional

import requests
from pymongo.database import Database
from .mongo_interface import USERS_COLLECTION

__all__ = ["authenticate_username"]


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


def is_user_authenticated(cookie: str, database: Database) -> bool:
    """Check if the user is authenticated in the web service."""
    col = database[USERS_COLLECTION]
    user_data = json.loads(cookie)
    data = col.find_one({key: user_data[key] for key in {"username", "token"}})
    return False if data is None else True
