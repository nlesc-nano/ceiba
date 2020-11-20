"""Test the authentication functionality."""

from pytest_mock import MockerFixture

from insilicoserver.user_authentication import authenticate_username


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
