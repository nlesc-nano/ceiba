"""Module to resolve the queries.

API
---

.. autofunction:: resolver_query_properties
.. autofunction:: resolver_query_jobs

"""
from typing import Any, Dict, List, Optional

from tartiflette import Resolver
from more_itertools import take
from insilicodatabase import (fetch_many_from_collection,
                              update_many_in_collection)

__all__ = ["resolver_query_jobs", "resolver_query_properties"]


@Resolver("Query.properties")
async def resolver_query_properties(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning Properties based on their `collection_name`.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    data = fetch_many_from_collection(ctx["mongodb"], args["collection_name"])
    return list(data)


@Resolver("Query.jobs")
async def resolver_query_jobs(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> List[Dict[str, Any]]:
    """
    Resolver in charge of returning jobs based on their status.

    Parameters
    ----------
    paren
        initial value filled in to the engine `execute` method
    args
        computed arguments related to the field
    ctx
        context filled in at engine initialization
    info
        information related to the execution and field resolution

    Returns
    -------
    The list of all jobs with the given status.
    """
    # metadata to query the jobs
    query = {"status": args["status"]}
    property_collection = args["collection_name"]
    jobs_collection = f"jobs_{property_collection}"

    # return an iterator to the jobs
    data = fetch_many_from_collection(ctx["mongodb"], jobs_collection, query=query)
    jobs = take(args["max_jobs"], data)

    # Mark the jobs as RESERVED
    prop_ids = [j["_id"] for j in jobs]
    query = {"_id": {"$in": prop_ids}}
    update = {"$set": {"status": "RESERVED"}}
    update_many_in_collection(ctx["mongodb"], jobs_collection, query, update)

    return jobs
