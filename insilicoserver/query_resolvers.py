"""Module to resolve the queries.

API
---

.. autofunction:: resolver_query_properties
.. autofunction:: resolver_query_jobs

"""
from typing import Any, Dict, Iterable, List, Optional

from more_itertools import take
from pymongo.collection import Collection
from tartiflette import Resolver


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
    collection = ctx["mongodb"][args["collection_name"]]
    data = collection.find()
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
    collection = ctx["mongodb"][jobs_collection]

    # Return the first available jobs
    if args["job_size"] is None:
        data = collection.find(query)
    # Return a small or large job if the user requested so
    else:
        data = get_jobs_by_size(args["job_size"], collection)

    jobs = take(args["max_jobs"], data)

    return jobs


def get_jobs_by_size(job_size: str, collection: Collection) -> Iterable[Dict[str, Any]]:
    """Retrieve jobs by size."""
    order = 1 if job_size == "SMALL" else -1
    cursor = collection.aggregate([
        {"$addFields": {
            "lensmile": {"$strLenCP": "$property.smile"}}},
        {"$sort": {"lensmile": order}}
    ])

    return cursor
