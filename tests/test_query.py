"""Test the query interface."""

import pytest

from ceiba.query_resolvers import (resolver_query_collections,
                                   resolver_query_jobs,
                                   resolver_query_properties)

from .utils_test import (MockedCollection, MockedDatabase,
                         read_properperties_and_jobs)

PARENT = None
INFO = None

MOCKED_DATA = read_properperties_and_jobs()


@pytest.mark.asyncio
async def test_query_properties():
    """Test the properties query resolver."""
    mocked_properties = MOCKED_DATA["PROPERTIES"].copy()
    ctx = {"mongodb": {"awesome_data": MockedCollection(mocked_properties)}}
    args = {"collection_name": "awesome_data"}
    results = await resolver_query_properties(PARENT, args, ctx, INFO)
    print("received results: ", results)
    first = results[0]
    assert all((first['metadata']['smile'] == "O=O", first['_id'] == 0))


@pytest.mark.asyncio
async def test_query_jobs():
    """Test the job query resolver."""
    args = {"status": "DONE", "max_jobs": 10, "collection_name": "awesome_data", "job_size": None}
    mocked_jobs = MOCKED_DATA["JOBS"].copy()
    ctx = {"mongodb": {"jobs_awesome_data": MockedCollection(mocked_jobs)}}

    jobs = await resolver_query_jobs(PARENT, args, ctx, INFO)
    first = jobs[0]
    assert first["_id"] == 33444


@pytest.mark.asyncio
async def test_query_collections():
    """Test the job query resolver."""
    data = MockedDatabase({"collection_foo": 3, "collection_bar": 2})
    ctx = {"mongodb": data}
    cols = await resolver_query_collections(PARENT, None, ctx, INFO)
    assert len(cols) == 2
    assert cols[0]['name'] == "collection_foo"
