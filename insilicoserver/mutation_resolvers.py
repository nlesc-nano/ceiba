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
from insilicodatabase import (fetch_one_from_collection,
                              store_data_in_collection,
                              update_one_in_collection)

from .data import JOBS

logger = logging.getLogger(__name__)


@Resolver("Mutation.createJob")
async def resolve_mutation_add_job(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
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
    jobs_collection = f"jobs_{property_collection}"

    # Try to store property. If a property with the same identifier exists
    # then return it without modifying the existing property
    query = {"_id": property_data["_id"]}
    prop = fetch_one_from_collection(database, property_collection, query)
    if prop is None:
        store_data_in_collection(database, property_collection, property_data)
        logger.info(f"Stored property with id {property_data['_id']} into collection {property_collection}")

    # Search if the job already exists. If the job already exists return its identifier
    query = {"property._id": property_data["_id"]}
    job_data = fetch_one_from_collection(database, jobs_collection, query)
    if job_data is None:
        # Extract job metadataa
        job_data = args['input']
        # Add reference to property
        job_data["property"] = DBRef(collection=property_collection, id=property_data["_id"])
        # Store job data
        job_data = args["input"]
        job_data["property"] = {key: property_data[key] for key in ("_id", "smile", "collection_name")}
        # Save jobs into the database
        job_id = store_data_in_collection(database, jobs_collection, job_data)
        logger.info(f"Stored job with id {job_id} into collection {jobs_collection}")

    return job_data


@Resolver("Mutation.updateJob")
async def resolve_mutation_update_job(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
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
        info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """Resolver in charge of updating a given job.

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
    job_data = args['input']
    jobs_collection = f"jobs_{job_data['collection_name']}"

    # Retrieve the job
    query = {"_id": job_data["_id"]}
    prop = fetch_one_from_collection(database, jobs_collection, query)
    if prop is None:
        raise RuntimeError(f"There is not job with id: {job_data['_id']} in the database!")

    update = {"$set": {"status": job_data['status']}}
    update_one_in_collection(database, jobs_collection, query, update)

    return None
