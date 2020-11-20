"""Test the mutation resolvers."""

import itertools
import json
from typing import Any, Dict

import pytest
from pytest_mock import MockFixture

from insilicoserver.mongo_interface import USERS_COLLECTION
from insilicoserver.mutation_resolvers import (
    resolve_mutation_add_job, resolve_mutation_authentication,
    resolve_mutation_update_job, resolve_mutation_update_job_status,
    resolve_mutation_update_property)

from .utils_test import MockedCollection, read_jobs

# Constant to mock the call
PARENT = None
INFO = None
COOKIE = '{"username": "felipeZ", "token": "Token"}'


def check_reply(reply: Dict[str, str]) -> None:
    """Check that the reply has a valid form."""
    assert all(x in reply.keys() for x in {"status", "text"})


@pytest.mark.asyncio
async def test_mutation_add_job(mocker: MockFixture):
    """Test the resolver for adding jobs."""
    job = read_jobs()[1]

    args = {"input": job, "cookie": COOKIE}
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(job),
        "awesome_data": MockedCollection(None)}}

    mocker.patch("insilicoserver.mutation_resolvers.is_user_authenticated", return_value=True)
    reply = await resolve_mutation_add_job(PARENT, args, ctx, INFO)
    check_reply(reply)


@pytest.mark.asyncio
async def test_mutation_add_nonexisting_job(mocker: MockFixture):
    """Test the resolver for adding jobs."""
    job = read_jobs()[1]

    args = {"input": job, 'cookie': COOKIE}
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(None),
        "awesome_data": MockedCollection(None)}}

    mocker.patch("insilicoserver.mutation_resolvers.is_user_authenticated", return_value=True)
    reply = await resolve_mutation_add_job(PARENT, args, ctx, INFO)
    check_reply(reply)


async def run_mutation_update_job(
        policy: str, new: Dict[str, Any], old: Dict[str, Any]) -> Dict[str, Any]:
    """Test the resolver for updating jobs."""
    args = {
        "input": new,
        'cookie': COOKIE,
        "duplication_policy": policy
    }
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(old),
        "awesome_data": MockedCollection({'data': '{"prop": 42}'})}}

    reply = await resolve_mutation_update_job(PARENT, args, ctx, INFO)
    return reply


@pytest.mark.asyncio
async def test_mutation_update_job(mocker: MockFixture):
    """Test the resolver for updating jobs."""
    mocker.patch("insilicoserver.mutation_resolvers.is_user_authenticated", return_value=True)
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
async def test_mutation_update_job_status(mocker: MockFixture):
    """Check the job status updater."""
    args = {"input": {
        "_id": 3141592,
        "collection_name": "awesome_data",
        "status": "RESERVED"},
        'cookie': COOKIE
    }
    # Mock database
    ctx = {"mongodb": {
        "jobs_awesome_data": MockedCollection(read_jobs())}}

    mocker.patch("insilicoserver.mutation_resolvers.is_user_authenticated", return_value=True)
    reply = await resolve_mutation_update_job_status(PARENT, args, ctx, INFO)
    assert reply['status'] == 'DONE'


@pytest.mark.asyncio
async def test_mutation_update_property(mocker: MockFixture):
    """Check the job status updater."""
    args = {"input": {
        "_id": 101010,
        "collection_name": "awesome_data",
        "data": '{"pi": "3.14159265358979323846"}'},
        'cookie': COOKIE}
    # Mock database
    ctx = {"mongodb": {
        "awesome_data": MockedCollection(None)}}

    mocker.patch("insilicoserver.mutation_resolvers.is_user_authenticated", return_value=True)
    reply = await resolve_mutation_update_property(PARENT, args, ctx, INFO)
    assert reply['status'] == 'DONE'


@pytest.mark.asyncio
async def test_mutation_authentication_invalid_token():
    """Check the authentication resolver for an invalid_token."""
    args = {"token": "InvalidToken"}
    # Mock database
    ctx = {"mongodb": {
        USERS_COLLECTION: MockedCollection(None)}}

    reply = await resolve_mutation_authentication(PARENT, args, ctx, INFO)
    assert reply['status'] == "FAILED"
    assert "Invalid Token" in reply['text']


@pytest.mark.asyncio
async def test_mutation_authentication_invalid_user(mocker: MockFixture):
    """Check the authentication resolver for an invalid_token."""
    args = {"token": "VeryLongToken"}
    # Mock database
    ctx = {"mongodb": {
        USERS_COLLECTION: MockedCollection(None)}}

    mocker.patch("insilicoserver.mutation_resolvers.authenticate_username", return_value="someone")
    reply = await resolve_mutation_authentication(PARENT, args, ctx, INFO)
    assert reply['status'] == "FAILED"
    assert "doesn't have permissions" in reply['text']


@pytest.mark.asyncio
async def test_mutation_authentication_valid_user(mocker: MockFixture):
    """Check the authentication resolver for an invalid_token."""
    args = {"token": "RosalindToken"}
    # Mock database
    ctx = {"mongodb": {
        USERS_COLLECTION: MockedCollection({"username": "RosalindFranklin"})}}

    mocker.patch("insilicoserver.mutation_resolvers.authenticate_username", return_value="RosalindFranklin")
    reply = await resolve_mutation_authentication(PARENT, args, ctx, INFO)
    cookie = json.loads(reply['text'])
    assert reply['status'] == "DONE"
    assert cookie['username'] == "RosalindFranklin"
