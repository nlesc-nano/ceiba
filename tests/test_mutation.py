"""Test the mutation resolvers."""

import pytest
from pytest_mock import MockFixture

from insilicoserver.mutation_resolvers import (
    resolve_mutation_add_job, resolve_mutation_update_job,
    resolve_mutation_update_job_status)

from .utils_test import read_jobs

PARENT = None
INFO = None
CONTEXT = {"mongodb": "mock"}
MOCKED_JOBS = read_jobs()


@pytest.mark.asyncio
async def test_mutation_add_job(mocker: MockFixture):
    """Test the resolver for adding jobs."""
    job = MOCKED_JOBS[1]
    job_id = job["_id"]

    args = {"input": job}
    # Mock the interaction with the database
    mocker.patch(
        "insilicoserver.mutation_resolvers.fetch_one_from_collection",
        return_value=None)
    mocker.patch(
        "insilicoserver.mutation_resolvers.store_one_in_collection", return_value=job_id)

    job = await resolve_mutation_add_job(PARENT, args, CONTEXT, INFO)
    print(job)
    assert all(job[key] == val for key, val in [("status", job["status"]), ("_id", job_id)])


@pytest.mark.asyncio
async def test_mutation_update_job(mocker: MockFixture):
    """Test the resolver for updating jobs."""
    args = {
        "input": MOCKED_JOBS[0]
    }

    # Mock the interaction with the database
    mocker.patch(
        "insilicoserver.mutation_resolvers.check_entry_existence", return_value=None)
    mocker.patch(
        "insilicoserver.mutation_resolvers.update_entry", return_value=None)

    job = await resolve_mutation_update_job(PARENT, args, CONTEXT, INFO)
    print(job)

    assert all(job[key] == val for key, val in [("status", "DONE"), ("_id", 33444)])


@pytest.mark.asyncio
async def test_mutation_update_job_status(mocker: MockFixture):
    """Check the job status updater."""
    args = {"input": {
        "_id": 3141592,
        "collection_name": "awesome_results",
        "status": "RESERVED"}
    }
    # Mock the interaction with the database
    mocker.patch(
        "insilicoserver.mutation_resolvers.check_entry_existence", return_value=None)

    mocker.patch(
        "insilicoserver.mutation_resolvers.update_one_in_collection", return_value=None)

    state = await resolve_mutation_update_job_status(PARENT, args, CONTEXT, INFO)
    assert state is None
