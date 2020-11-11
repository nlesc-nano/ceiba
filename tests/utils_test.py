"""Functions use for testing."""

import json
from pathlib import Path
from typing import Any, Dict, List

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
    new_jobs = []
    for job, prop in zip(jobs, properties):
        job["property"] = prop
        new_jobs.append(job)
    return new_jobs


class MockInsertion:
    """Mock the result of inserting some data in a collection."""

    def inserted_id(self) -> int:
        return 42


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

    def insert_one(self, query: Dict[str, Any]) -> MockInsertion:
        return MockInsertion()

    def estimated_document_count(self) -> int:
        return 42


class MockedDatabase:
    """Mock a Mongodb database."""
    def __init__(self, data: Dict[str, Any]) -> None:
        self.data = data

    def list_collection_names(self) -> List[str]:
        return list(self.data.keys())

    def __getitem__(self, item: str) -> MockedCollection:
        return MockedCollection({})
