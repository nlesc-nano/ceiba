"""Test the app instantiation."""

import argparse
import sys
from pathlib import Path

import pytest
from pytest_mock import MockFixture

from ceiba.app import configure_logger, create_context, read_cli_args

from .utils_test import PATH_TEST

PATH_USERS = PATH_TEST / "users.txt"

CLI_ARGS = argparse.Namespace(
    file=PATH_USERS, mongo_url="localhost", username="juan", password="42")


def test_cli_parser(mocker: MockFixture):
    """Test that the CLI arguments are parsed correctly."""
    sys.argv = ["ceiba", "-f", PATH_USERS.absolute().as_posix(),
                "-u", "RosalindFranklin", "-p", '42']
    args = read_cli_args()
    assert args.username == "RosalindFranklin" and args.password == "42"


def test_nonexisting_user_file(mocker: MockFixture):
    """Check that an error is raised if a nonexisting file is passed."""
    sys.argv = ["ceiba", "-f", "Nowhere/Nonexistingfile",
                "-u", "RosalindFranklin", "-p", '42']

    with pytest.raises(SystemExit) as info:
        read_cli_args()

    error = info.value.args[0]
    print("err: ", error)


def test_create_context(mocker: MockFixture):
    """Test context generation."""
    mocker.patch("ceiba.app.connect_to_db", return_value="mock")
    mocker.patch("ceiba.app.add_users_to_db", return_value=None)
    ctx = create_context(CLI_ARGS)
    assert "mongodb" in ctx


def test_logger(tmp_path: Path):
    """Check the logger."""
    workdir = Path(tmp_path)
    configure_logger(workdir, "ceiba")
