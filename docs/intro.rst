
The Ceiba Web Service
########################
🧬🧪  Most of the scientific simulations are usually performed in supercomputer
or high tech facilities. Usually the data is kept on those facilities
stored in a raw format, 🗝  in contradiction with the
`scientific FAIR principles for data <https://www.go-fair.org/fair-principles/>`_.

This repo contains a library to create a web service to interact with a database
containing a set of numerical properties.All the interactions with the database are
defined by a `GraphQL API <https://graphql.org/>`_ and the service is developed using `tartiflette <https://tartiflette.io/>`_


Interactions with the database
##############################
Using the `GraphQL query language <https://graphql.org/>`_  the service
define a set of rules to interact with the services: **queries** and **mutations**.

The queries are just read only actions against the database, while the mutations,
involved some change in the database state.
