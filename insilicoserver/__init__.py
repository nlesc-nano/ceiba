"""Library API."""

import logging

from .__version__ import __version__
from .mutation_resolvers import (resolve_mutation_add_job,
                                 resolve_mutation_update_job,
                                 resolve_mutation_update_job_status)
from .query_resolvers import resolver_query_jobs

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Felipe Zapata"
__email__ = 'f.zapata@esciencecenter.nl'

__all__ = ["resolver_query_jobs", "resolve_mutation_add_job", "resolve_mutation_update_job",
           "resolve_mutation_update_job_status"]
