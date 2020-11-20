"""Test the authentication functionality."""

from pytest_mock import MockerFixture

from insilicoserver.user_authentication import authenticate_username
from insilicoserver.mongo_interface import USERS_COLLECTION, add_users_to_db

from .test_mongo_interface import get_database
from .utils_test import PATH_TEST


class MockReply(dict):
    """Mock requests reply."""
    def __getattr__(self, attr):
        """Allow `obj.key` notation."""
        return self.get(attr)


def test_github_user():
    """Check that None is return if an invalid toke is provided."""
    username = authenticate_username("invalidtoken123")
    assert username is None


def test_correct_token(mocker: MockerFixture):
    """Check that a username is returns if a valid token is provided."""
    mocked_reply = MockReply(
        {"status_code": 200, "text": '{"data": {"viewer": {"login": "felipeZ"}}}'})
    mocker.patch("requests.post", return_value=mocked_reply)
    username = authenticate_username("validtoken")

    assert username == "felipeZ"


def test_add_user_to_db():
    """Check that some users are properly added in the database."""
    path_users = PATH_TEST / "users.txt"

    try:
        db = get_database()
        add_users_to_db(db, path_users)
    finally:
        db.drop_collection(USERS_COLLECTION)