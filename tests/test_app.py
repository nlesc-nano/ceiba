"""Test the app instantiation."""

import argparse
import logging
import sys
from pathlib import Path

from pytest_mock import MockFixture

from insilicoserver.app import configure_logger, create_context, read_cli_args

CLI_ARGS = argparse.Namespace(username="juan", password="42")


def test_cli_parser(mocker: MockFixture):
    """Test that the CLI arguments are parsed correctly."""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=CLI_ARGS)
    args = read_cli_args()
    print("args: ", args)
    assert args.username == "juan" and args.password == "42"


def test_create_context(mocker: MockFixture):
    """Test context generation."""
    mocker.patch("insilicoserver.app.connect_to_db", return_value="mock")
    ctx = create_context(CLI_ARGS)
    assert "mongodb" in ctx


def test_run_app(mocker: MockFixture):
    """Test that the app starts normally."""
    mocker.patch("argparse.ArgumentParser.parse_args", return_value=CLI_ARGS)
    mocker.patch("insilicoserver.app.connect_to_db", return_value="mock")


def test_logger(tmp_path: Path):
    """Check the logger."""
    workdir = Path(tmp_path)
    configure_logger(workdir, "insilicoserver")
