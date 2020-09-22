"""Module to change data in database.

API
---
"""
from typing import Any, Dict, Optional

from tartiflette import Resolver

from properties_server.data import JOBS


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