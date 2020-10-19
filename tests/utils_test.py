"""Functions use for testing."""

import json
from pathlib import Path
from typing import Any, Dict, Optional

import pkg_resources as pkg

__all__ = ["PATH_INSILICOSERVER", "PATH_TEST", "read_jobs", "read_properperties_and_jobs"]

# Environment data
PATH_INSILICOSERVER = Path(pkg.resource_filename('insilicoserver', ''))
ROOT = PATH_INSILICOSERVER.parent

PATH_TEST = ROOT / "tests" / "files"


def read_properperties_and_jobs() -> Dict[str, Any]:
    """Read the mocked data."""
    path_data = PATH_TEST / "mocked_data.json"
    with open(path_data, 'r') as handler:
        return json.load(handler)


def read_jobs() -> Dict[str, Any]:
    """Get the mock data for the jobs."""
    data = read_properperties_and_jobs()
    jobs = data["JOBS"]
    properties = data["PROPERTIES"]

    # Add property attribute to the jobs
    for job, prop in zip(jobs, properties):
        job["property"] = prop

    return jobs


class MockedCollection:
    """Mock a Mongodb collection."""

    def __init__(self, data: Any) -> None:
        self.data = data

    def find_one(self, query: Any = None) -> Any:
        return self.data

    def find(self, query: Any = None) -> Any:
        return self.data

    def update_one(self, query: Dict[str, Any], update: Dict[str, Any]) -> None:
        return None

    def insert_one(self, query: Dict[str, Any]) -> None:
        return None