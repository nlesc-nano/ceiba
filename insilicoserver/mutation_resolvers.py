"""Module to change data in database.

API
---
.. autofunction:: resolve_mutation_add_job
.. autofunction:: resolve_mutation_update_job
.. autofunction:: resolve_mutation_update_job_status
.. autofunction:: resolve_mutation_update_property

"""
import logging
from typing import Any, Dict, Optional, Set

from bson.dbref import DBRef
from tartiflette import Resolver
from insilicodatabase import (fetch_one_from_collection,
                              store_one_in_collection,
                              update_one_in_collection)


__all__ = ["resolve_mutation_add_job", "resolve_mutation_update_job",
           "resolve_mutation_update_job_status", "resolve_mutation_update_property"]

logger = logging.getLogger(__name__)

@Resolver("Mutation.updateProperty")
async def resolve_mutation_update_property(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Resolver in charge of Updating or creating a property in the database.

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
    Update
    """
    database = ctx["mongodb"]
    # Extract property data
    property_data = args['input']

    # Update the following keywords
    prop_mutable_keywords = {"data", "input", "geometry"}
    update_entry(database, property_data["collection_name"], property_data, prop_mutable_keywords)


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
    Updated Property
    """
    database = ctx["mongodb"]
    # Extract property data
    property_data = args['input'].pop('property')
    property_collection = property_data["collection_name"]
    jobs_collection = f"jobs_{property_collection}"

    # Try to store property.
    store_property(database, property_data)

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
        job_id = store_one_in_collection(database, jobs_collection, job_data)
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
    Updated job
    """
    database = ctx["mongodb"]
    # Extract property data and Filter non-null data
    job_data = {key: val for key, val in args["input"].items() if val is not None}
    prop_data = {key: val for key, val in job_data.pop("property").items() if val is not None}
    jobs_collection = f"jobs_{prop_data['collection_name']}"

    # Check that the job exists
    check_entry_existence(database, jobs_collection, job_data["_id"])

    # Check that the property exists
    check_entry_existence(database, prop_data["collection_name"], prop_data["_id"])
    job_mutable_keywords = {"status", "user", "platform", "report_time"}
    update_entry(database, jobs_collection, job_data, job_mutable_keywords)

    # Update property state
    if job_data['status'] == "DONE":
        prop_mutable_keywords = {"data", "input", "geometry"}
        update_entry(database, prop_data["collection_name"], prop_data, prop_mutable_keywords)

    return args["input"]


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
    Updated job
    """
    database = ctx["mongodb"]
    # Extract property data
    job_data = args['input']
    jobs_collection = f"jobs_{job_data['collection_name']}"

    # Retrieve the job
    check_entry_existence(database, jobs_collection, job_data["_id"])

    # Update job status
    query = {"_id": job_data["_id"]}
    update = {"$set": {"status": job_data['status']}}
    update_one_in_collection(database, jobs_collection, query, update)

    return None


def check_entry_existence(database: Any, collection_name: str, identifier: int) -> None:
    """Search for a jobs in the ``database`` raise error if no job is found."""
    query = {"_id": identifier}
    job = fetch_one_from_collection(database, collection_name, query)
    if job is None:
        raise RuntimeError(f"There is not job with id: {identifier} in the database!")


def update_entry(
        database: Any, collection_name: str, entry: Dict[str, Any],
        mutable_keywords: Set[str]) -> None:
    """Update an entry in the collection changing only the allow keywords."""
    entry_updates = {key: entry[key] for key in entry.keys() if key in mutable_keywords}
    query = {"_id": entry["_id"]}
    update = {"$set": entry_updates}
    update_one_in_collection(database, collection_name, query, update)


def store_property(database: Any, property_data: Dict[str, Any]) -> None:
    """Store property if not already available in the database."""
    # If a property with the same identifier exists
    # then return it without modifying the existing property
    property_collection = property_data["collection_name"]
    index = property_data["_id"]
    query = {"_id": index}
    prop = fetch_one_from_collection(database, property_collection, query)
    if prop is None:
        store_one_in_collection(database, property_collection, property_data)
        logger.info(f"Stored property with id {index} into collection {property_collection}")
