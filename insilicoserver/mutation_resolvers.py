"""Module to change data in database.

API
---
.. autofunction:: resolve_mutation_add_job
.. autofunction:: resolve_mutation_authentication
.. autofunction:: resolve_mutation_update_job
.. autofunction:: resolve_mutation_update_job_status
.. autofunction:: resolve_mutation_update_property

"""
import json
import logging
import secrets
from datetime import datetime
from typing import Any, Dict, Optional, Set

from tartiflette import Resolver
from pymongo.database import Database
from pymongo.collection import Collection

from .user_authentication import authenticate_username, is_user_authenticated
from .mongo_interface import USERS_COLLECTION


__all__ = ["resolve_mutation_add_job", "resolve_mutation_update_job",
           "resolve_mutation_update_job_status", "resolve_mutation_update_property"]

logger = logging.getLogger(__name__)

PROPERTY_MUTABLE_KEYWORDS = {"data", "input", "geometry", "large_objects"}
JOB_MUTABLE_KEYWORDS = {"status", "user", "platform", "report_time", "schedule_time"}
AUTHENTICATION_ERROR_MESSAGE = {"status": "FAILED", "text": "The user is not authenticated"}


@Resolver("Mutation.authenticateUser")
async def resolve_mutation_authentication(
    parent: Optional[Any],
    args: Dict[str, Any],
    ctx: Dict[str, Any],
    info: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Resolver to authenticate a user.

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
    Temporal token to authenticate the user or failure message

"""
    # Extract property data
    token = args['token']
    known_user = authenticate_username(token)
    if known_user is None:
        return {"status": "FAILED", "text": "Invalid Token!"}

    database = ctx["mongodb"]
    # Check if the user is allowed to interact with the service
    collection = database[USERS_COLLECTION]
    user_data = collection.find_one({"username": known_user})
    if user_data is None:
        msg = f"User `{known_user}` doesn't have permissions to access the service"
        return {"status": "FAILED",
                "text": msg}

    # Update the token used to authenticate the client
    reply_token = secrets.token_hex(16)

    filter_name = {"username": known_user}
    entry = {"token": reply_token, "username": known_user,
             "time": datetime.now()}

    # Insert new entry if not previously find
    collection.replace_one(filter_name, entry)

    cookie = json.dumps({"username": known_user, "token": reply_token})

    return {"status": "DONE", "text": cookie}


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
    Message with the status of the update

    """
    database = ctx["mongodb"]
    # Check if the user is authenticated
    if not is_user_authenticated(args['cookie'], database):
        return AUTHENTICATION_ERROR_MESSAGE

    # Extract property data
    property_data = args['input']

    # Update the following keywords
    collection = database[property_data["collection_name"]]
    update_entry(collection, property_data, PROPERTY_MUTABLE_KEYWORDS)

    return {"status": "DONE"}


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
    Status message
    """
    database = ctx["mongodb"]
    # Check if the user is authenticated
    if not is_user_authenticated(args['cookie'], database):
        return AUTHENTICATION_ERROR_MESSAGE

    # Extract property data
    property_data = args['input'].pop('property')
    property_collection = property_data["collection_name"]
    jobs_collection = database[f"jobs_{property_collection}"]

    # Try to store property.
    store_property(database, property_data)

    # Search if the job already exists. If the job already exists return its identifier
    query = {"property._id": property_data["_id"]}

    job_data = jobs_collection.find_one(query)
    if job_data is None:
        # Extract job metadataa
        job_data = args['input']
        job_data["property"] = {
            key: property_data[key] for key in ("_id", "smile", "collection_name")}
        # Save jobs into the database
        job_id = jobs_collection.insert_one(job_data).inserted_id
        msg = f"Stored job with id {job_id} into collection jobs_{property_data['collection_name']}"
    else:
        msg = f"Job with id {job_data['_id']} is already in collection jobs_{property_data['collection_name']}"

    return {"status": "DONE", "text": msg}


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
    # Check if the user is authenticated
    if not is_user_authenticated(args['cookie'], database):
        return AUTHENTICATION_ERROR_MESSAGE

    msg = ""

    # Extract property data and Filter non-null data
    job_data = {key: val for key, val in args["input"].items() if val is not None}
    prop_data = {key: val for key, val in job_data.pop("property").items() if val is not None}

    # Extract collections
    jobs_collection = database[f"jobs_{prop_data['collection_name']}"]
    prop_collection = database[prop_data["collection_name"]]

    # Check that the job exists
    old_job = check_entry_existence(jobs_collection, job_data["_id"])
    # Report new data
    if old_job["status"] != "DONE" and job_data['status'] == "DONE":
        update_entry(jobs_collection, job_data, JOB_MUTABLE_KEYWORDS)

    # Check that the property exists
    old_prop = check_entry_existence(prop_collection, prop_data["_id"])

    # Update property state
    if old_job['status'] != "DONE" and job_data['status'] == "DONE":
        update_entry(prop_collection, prop_data, PROPERTY_MUTABLE_KEYWORDS)
        msg = f"""The property with id {prop_data['_id']}, has been added to collection {prop_data['collection_name']}"""
    # There is a new job
    elif old_job['status'] == "DONE" and job_data['status'] == "DONE":
        handle_duplication(prop_collection, prop_data, old_prop, args["duplication_policy"])
        msg = f"""Properties with id: {prop_data['_id']} have been previously reported.
The new properties are handled using the {args['duplication_policy']} duplication policy"""

    elif old_job['status'] != "DONE" and job_data['status'] != "DONE":
        msg = """Neither the old or the new job have succeeded, nothing new to report!"""

    return {"status": "DONE", "text": msg}


@Resolver("Mutation.updateJobStatus")
async def resolve_mutation_update_job_status(
        parent: Optional[Any],
        args: Dict[str, Any],
        ctx: Dict[str, Any],
        info: Dict[str, Any]) -> Dict[str, Any]:
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
    Status message

    """
    database = ctx["mongodb"]
    # Check if the user is authenticated
    if not is_user_authenticated(args['cookie'], database):
        return AUTHENTICATION_ERROR_MESSAGE

    # Extract property data
    job_data = args['input']
    jobs_collection = database[f"jobs_{job_data['collection_name']}"]

    # Retrieve the job
    check_entry_existence(jobs_collection, job_data["_id"])

    # Update job status
    update_entry(jobs_collection, job_data, JOB_MUTABLE_KEYWORDS)

    return {"status": "DONE"}


def handle_duplication(
        collection: Collection, prop_data: Dict[str, Any], old_prop: Dict[str, Any],
        duplication_policy: str) -> None:
    """Take care of the duplicated data following the user policy."""
    if duplication_policy == "OVERWRITE":
        update_entry(collection, prop_data, PROPERTY_MUTABLE_KEYWORDS)
    elif duplication_policy == "MERGE":
        prop_data['data'] = merge_json_data(prop_data['data'], old_prop['data'])
        update_entry(collection, prop_data, PROPERTY_MUTABLE_KEYWORDS)
    elif duplication_policy == "APPEND":
        raise NotImplementedError("Append policy has not been implemented")


def check_entry_existence(collection: Collection, identifier: int) -> Dict[str, Any]:
    """Search for a jobs in the ``database`` raise error if no job is found."""
    query = {"_id": identifier}
    job = collection.find_one(query)
    if job is None:
        raise RuntimeError(f"There is not element with id: {identifier} in the database!")

    return job


def update_entry(
        collection: Collection, entry: Dict[str, Any],
        mutable_keywords: Set[str]) -> None:
    """Update an entry in the collection changing only the allow keywords."""
    entry_updates = {key: entry[key] for key in entry.keys() if key in mutable_keywords}
    query = {"_id": entry["_id"]}
    update = {"$set": entry_updates}
    collection.update_one(query, update)


def store_property(database: Database, property_data: Dict[str, Any]) -> None:
    """Store property if not already available in the database.

    If a property with the same identifier exists
    then return it without modifying the existing property.
    """
    property_collection = database[property_data["collection_name"]]
    index = property_data["_id"]
    query = {"_id": index}
    prop = property_collection.find_one(query)
    if prop is None:
        property_collection.insert_one(property_data)
        logger.info(f"Stored property with id {index} into collection {property_collection}")


def merge_json_data(old_data: str, new_data: str) -> str:
    """Merge to dictionaries encoded as JSON."""
    if not old_data:
        return new_data

    data = json.loads(old_data)
    data.update(json.loads(new_data))
    return json.dumps(data)
