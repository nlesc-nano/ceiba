"""Module to change data in database.

API
---
.. autofunction:: resolve_mutation_add_job
.. autofunction:: resolve_mutation_update_job
.. autofunction:: resolve_mutation_update_job_status

"""
import logging
from typing import Any, Dict, Optional

from bson.dbref import DBRef
from tartiflette import Resolver
from insilicodatabase import store_data_in_collection

from .data import JOBS

logger = logging.getLogger(__name__)


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
    property_data["_id"] = property_data["id"]
    property_id = store_data_in_collection(database, property_collection, property_data)
    logger.info(f"Stored property with id {property_data['_id']} into collection {property_collection}")

    # Extract job metadata
    job_data = args['input']
    # Add mongo identifier
    job_data["_id"] = job_data["id"]

    # Add reference to property
    jobs_collection = f"jobs_{property_collection}"
    job_data["property"] = DBRef(collection=property_collection, id=property_id)
    # Store job data
    job_data = args["input"]
    job_id = store_data_in_collection(database, jobs_collection, job_data)
    logger.info(f"Stored job with id {job_id} into collection {jobs_collection}")
    job_data["property"] = {key: property_data[key] for key in ("id", "smile", "collection_name")}
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
