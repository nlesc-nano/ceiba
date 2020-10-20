"""Test the mutation resolvers."""

from typing import Any, Dict

import pytest

from insilicoserver.mutation_resolvers import (
    resolve_mutation_add_job, resolve_mutation_update_job,
    resolve_mutation_update_job_status, resolve_mutation_update_property)

from .utils_test import MockedCollection, read_jobs

PARENT = None
INFO = None
MOCKED_JOBS = read_jobs()


@pytest.mark.asyncio
async def test_mutation_add_job():
    """Test the resolver for adding jobs."""
    job = MOCKED_JOBS[1]
    job_id = job["_id"]

    args = {"input": job}
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(MOCKED_JOBS[1]),
        "awesome_data": MockedCollection(None)}}

    job = await resolve_mutation_add_job(PARENT, args, ctx, INFO)
    assert all(job[key] == val for key, val in [("status", job["status"]), ("_id", job_id)])


async def run_mutation_update_job(policy: str) -> Dict[str, Any]:
    """Test the resolver for updating jobs."""
    args = {
        "input": MOCKED_JOBS[0],
        "duplication_policy": policy
    }
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(MOCKED_JOBS[0]),
        "awesome_data": MockedCollection({'data': '{"prop": 42}'})}}

    job = await resolve_mutation_update_job(PARENT, args, ctx, INFO)
    return job


@pytest.mark.asyncio
async def test_mutation_update_job():
    """Test the resolver for updating jobs."""
    # Test keep policy
    job = await run_mutation_update_job("KEEP")
    assert all(job[key] == val for key, val in [("status", "DONE"), ("_id", 33444)])

    # Test overwrite policy
    job = await run_mutation_update_job("OVERWRITE")
    assert all(job[key] == val for key, val in [("status", "DONE"), ("_id", 33444)])

    # Test merge policy
    job = await run_mutation_update_job("MERGE")
    assert all(job[key] == val for key, val in [("status", "DONE"), ("_id", 33444)])


@pytest.mark.asyncio
async def test_mutation_update_job_status():
    """Check the job status updater."""
    args = {"input": {
        "_id": 3141592,
        "collection_name": "awesome_data",
        "status": "RESERVED"}
    }
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(MOCKED_JOBS)}}

    reply = await resolve_mutation_update_job_status(PARENT, args, ctx, INFO)
    assert reply is None


@pytest.mark.asyncio
async def test_mutation_update_property():
    """Check the job status updater."""
    args = {"input": {
        "_id": 101010,
        "collection_name": "awesome_data",
        "data": '{"pi": "3.14159265358979323846"}'
    }}
    # Mock database
    ctx = {"mongodb": {
        "awesome_data": MockedCollection(None)}}

    reply = await resolve_mutation_update_property(PARENT, args, ctx, INFO)
    assert reply is None
