
The Insilico Web Service
########################
Most of the scientific simulations are usually performed in supercomputer
or high tech facilities. Usually the data is kept on those facilities
stored in a raw format, in contraction with the
`scientific FAIR principles for data <https://www.go-fair.org/fair-principles/>`_.

This web service provides an interface to store and retrieve data from a 
database, without the manual intervention of the researcher.

Interactions with the database
##############################
Using the `GraphQL query language <https://graphql.org/>`_  the service
define a set of rules to interact with the services: **queries** and **mutations**.

The queries are just read only actions against the database, while the mutations,
involved some change in the database state.