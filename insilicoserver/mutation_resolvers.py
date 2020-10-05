"""Module to change data in database.

API
---
.. autofunction:: resolve_mutation_add_job
.. autofunction:: resolve_mutation_update_job
.. autofunction:: resolve_mutation_update_job_status

"""
from typing import Any, Dict, Optional

from insilicodatabase import store_data_in_collection
from tartiflette import Resolver

from .data import JOBS


@Resolver("Mutation.createJob")
async def resolve_mutation_add_job(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Dict[str, Any]:
    """
    Resolver in charge of Creating a new job.

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
    Update job
    """
    database = ctx["mongodb"]
    # Extract property data
    property_data = args['input'].pop('property')
    property_collection = property_data["collection_name"]
    property_data["_id"] = property_data.pop("id")
    property_id = store_data_in_collection(database, property_collection, property_data)

    # Extract job metadata
    job_data = args['input']
    # Add mongo identifier
    job_data["_id"] = job_data["id"]

    # Add reference to property
    job_data["property"] = {"$ref": property_collection, "$db": database.name, "$id": property_id}
    job_data = args["input"]
    print(job_data)
    return job_data



@Resolver("Mutation.updateJob")
async def resolve_mutation_update_job(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: "ResolveInfo",
) -> Dict[str, Any]:
    """
    Resolver in charge of updating a given job

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
    Update job
    """
    job = next(x for x in JOBS if x["id"] == args["input"]["id"])
    return job


@Resolver("Mutation.updateJobStatus")
async def resolve_mutation_update_job_status(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: "ResolveInfo") -> Dict[str, Any]:
    """
    Resolver in charge of updating a given job

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
    Update job
    """
    job = next(x for x in JOBS if x["id"] == args["input"]["id"])
    return job
