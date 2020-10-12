"""Test the query interface."""

import pytest
from pytest_mock import MockFixture

from insilicoserver.query_resolvers import (resolver_query_jobs,
                                            resolver_query_properties)

from .utils_test import read_properperties_and_jobs

PARENT = None
INFO = None
CONTEXT = {"mongodb": "mock"}

MOCKED_DATA = read_properperties_and_jobs()


@pytest.mark.asyncio
async def test_query_properties(mocker: MockFixture):
    """Test the properties query resolver."""
    args = {"collection_name": "awesome_data"}
    mocked_properties = MOCKED_DATA["PROPERTIES"].copy()
    mocker.patch(
        "insilicoserver.query_resolvers.fetch_many_from_collection", return_value=mocked_properties)
    results = await resolver_query_properties(PARENT, args, CONTEXT, INFO)
    print("received results: ", results)
    first = results[0]
    assert all((first['smile'] == "O=O", first['_id'] == 0))


@pytest.mark.asyncio
async def test_query_jobs(mocker: MockFixture):
    """Test the job query resolver."""
    args = {"status": "DONE", "max_jobs": 10, "collection_name": "awesome_data"}
    mocked_jobs = MOCKED_DATA["JOBS"].copy()
    mocker.patch(
        "insilicoserver.query_resolvers.fetch_many_from_collection", return_value=mocked_jobs)
    mocker.patch(
        "insilicoserver.query_resolvers.update_many_in_collection", return_value=None)

    jobs = await resolver_query_jobs(PARENT, args, CONTEXT, INFO)
    first = jobs[0]
    assert first["_id"] == 33444
