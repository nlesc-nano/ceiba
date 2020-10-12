"""Test the query interface."""

import pytest

from insilicoserver.query_resolvers import (resolver_query_jobs,
                                            resolver_query_properties)


mocked_properties = [{'_id': 3141592, 'foo': 42, 'tux': 1618, 'status': "AVAILABLE"}]
PARENT = None
INFO = None
CONTEXT = {"mongodb": "mock"}


@pytest.mark.asyncio
async def test_query_properties(mocker):
    """Test the properties query resolver."""
    args = {"collection_name": "awesome_results"}
    mocker.patch(
        "insilicoserver.query_resolvers.fetch_many_from_collection", return_value=mocked_properties)
    results = await resolver_query_properties(PARENT, args, CONTEXT, INFO)
    print("received results: ", results)
    first = results[0]
    assert all((first['foo'] == 42, first['tux'] == 1618))


@pytest.mark.asyncio
async def test_query_jobs(mocker):
    """Test the job query resolver."""
    args = {"status": "DONE", "max_jobs": 10, "collection_name": "awesome_results"}
    mocker.patch(
        "insilicoserver.query_resolvers.fetch_many_from_collection", return_value=mocked_properties)
    mocker.patch(
        "insilicoserver.query_resolvers.update_many_in_collection", return_value=None)

    jobs = await resolver_query_jobs(PARENT, args, CONTEXT, INFO)
    first = jobs[0]
    assert first["_id"] == 3141592
