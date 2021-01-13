"""Main loop event.

.. autofunction:: run

"""

import argparse
import logging
from pathlib import Path
from typing import Any, Dict

import pkg_resources as pkg
from aiohttp import web
from tartiflette_aiohttp import register_graphql_handlers
from .mongo_interface import DatabaseConfig, add_users_to_db, connect_to_db

from .__version__ import __version__

__all__ = ["run"]

PATH_LIB = Path(pkg.resource_filename('ceiba', ''))
logger = logging.getLogger(__name__)


def create_context(args: argparse.Namespace) -> Dict[str, Any]:
    """Create context to run the app."""
    # Create Database
    db_info = DatabaseConfig(
        "properties", host=args.mongo_url, username=args.username, password=args.password)
    # Add Allow users
    database = connect_to_db(db_info)
    add_users_to_db(database, args.file)
    context = {
        "mongodb": connect_to_db(db_info)
    }
    return context


def configure_logger(workdir: Path, package_name: str) -> None:
    """Set the logging infrasctucture."""
    file_log = workdir / 'server.log'
    logging.basicConfig(filename=file_log, level=logging.INFO,
                        format='%(asctime)s  %(message)s',
                        datefmt='[%I:%M:%S]')
    handler = logging.StreamHandler()
    handler.terminator = ""

    path = pkg.resource_filename(package_name, '')

    logger.setLevel(logging.INFO)
    logger.info(f"Using {package_name} version: {__version__}\n")
    logger.info(f"{package_name} path is: {path}\n")
    logger.info(f"Working directory is: {workdir}")


def exists(input_file: str) -> Path:
    """Check if the input file exists."""
    path = Path(input_file)
    if not path.exists():
        raise argparse.ArgumentTypeError(f"{input_file} doesn't exist!")

    return path


def read_cli_args() -> argparse.Namespace:
    """Read the command line arguments."""
    parser = argparse.ArgumentParser("ceiba")
    parser.add_argument(
        '-f', "--file", required=True, type=exists, help="File with the allow users")
    parser.add_argument('-m', '--mongo_url', default="localhost")
    parser.add_argument('-u', '--username', default=None, help="mongo username")
    parser.add_argument('-p', '--password', default=None, help="mongo password")
    return parser.parse_args()


def run() -> None:
    """Entry point of the application."""
    configure_logger(Path("."), "ceiba")
    args = read_cli_args()
    web.run_app(
        register_graphql_handlers(
            app=web.Application(),
            executor_context=create_context(args),
            engine_sdl=(PATH_LIB / "sdl").absolute().as_posix(),
            engine_modules=[
                "ceiba.query_resolvers",
                "ceiba.mutation_resolvers",
                "ceiba.subscription_resolvers",
                "ceiba.directives.rate_limiting",
                "ceiba.directives.auth",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True
        )
    )
