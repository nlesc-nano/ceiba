"""Test the mutation resolvers."""

import itertools
from typing import Any, Dict

import pytest

from insilicoserver.mutation_resolvers import (
    resolve_mutation_add_job, resolve_mutation_update_job,
    resolve_mutation_update_job_status, resolve_mutation_update_property)

from .utils_test import MockedCollection, read_jobs

PARENT = None
INFO = None
MOCKED_JOBS = read_jobs()


def check_reply(reply: Dict[str, str]) -> None:
    """Check that the reply has a valid form."""
    assert all(x in reply.keys() for x in {"status", "text"})


@pytest.mark.asyncio
async def test_mutation_add_job():
    """Test the resolver for adding jobs."""
    job = MOCKED_JOBS[1]

    args = {"input": job}
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(MOCKED_JOBS[1]),
        "awesome_data": MockedCollection(None)}}

    reply = await resolve_mutation_add_job(PARENT, args, ctx, INFO)
    check_reply(reply)


async def run_mutation_update_job(
        policy: str, new: Dict[str, Any], old: Dict[str, Any]) -> Dict[str, Any]:
    """Test the resolver for updating jobs."""
    args = {
        "input": new,
        "duplication_policy": policy
    }
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(old),
        "awesome_data": MockedCollection({'data': '{"prop": 42}'})}}

    reply = await resolve_mutation_update_job(PARENT, args, ctx, INFO)
    return reply


@pytest.mark.asyncio
async def test_mutation_update_job():
    """Test the resolver for updating jobs."""
    # The first job is done the second available
    done_available = read_jobs()
    # Test keep policy
    for job1, job2 in itertools.product(done_available, done_available):
        reply = await run_mutation_update_job("KEEP", job1, job2)
        check_reply(reply)

    # Test overwrite policy
    for job1, job2 in itertools.product(done_available, done_available):
        reply = await run_mutation_update_job("OVERWRITE", job1, job2)
        check_reply(reply)

    # Test merge policy
    for job1, job2 in itertools.product(done_available, done_available):
        reply = await run_mutation_update_job("MERGE", job1, job2)
        check_reply(reply)


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
    assert reply['status'] == 'DONE'


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
    assert reply['status'] == 'DONE'
