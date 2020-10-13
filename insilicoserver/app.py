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
from insilicodatabase import DatabaseConfig, connect_to_db


from .__version__ import __version__

PATH_LIB = Path(pkg.resource_filename('insilicoserver', ''))


logger = logging.getLogger(__name__)


def create_context(args: argparse.Namespace) -> Dict[str, Any]:
    """Create context to run the app."""
    db_info = DatabaseConfig("properties", username=args.username, password=args.password)
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


def read_cli_args() -> argparse.Namespace:
    """Read the command line arguments."""
    parser = argparse.ArgumentParser("insilico-server")
    parser.add_argument('-u', '--username', default=None)
    parser.add_argument('-p', '--password', default=None)
    return parser.parse_args()


def run() -> None:
    """Entry point of the application."""
    configure_logger(Path("."), "insilicoserver")
    args = read_cli_args()
    web.run_app(
        register_graphql_handlers(
            app=web.Application(),
            executor_context=create_context(args),
            engine_sdl=(PATH_LIB / "sdl").absolute().as_posix(),
            engine_modules=[
                "insilicoserver.query_resolvers",
                "insilicoserver.mutation_resolvers",
                "insilicoserver.subscription_resolvers",
                "insilicoserver.directives.rate_limiting",
                "insilicoserver.directives.auth",
            ],
            executor_http_endpoint="/graphql",
            executor_http_methods=["POST"],
            graphiql_enabled=True
        )
    )
