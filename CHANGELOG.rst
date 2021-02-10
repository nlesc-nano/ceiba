##########
Change Log
##########

0.3.0 [Unreleased]
******************

0.2.0 [10/02/2021]
******************

New
---
* Add query resolver to retrieve the available collections
* Add mutation to authenticate user (#2)
* Add token to identify user (#6)
* Docker container recipe (#8)
* use `Caddy <https://caddyserver.com/>`_ to generate the certificate and the start the reverse-proxy (#12)
* Use `docker-compose to start the app <https://github.com/nlesc-nano/ceiba/issues/13>`_

CHANGED
-------
* Allow to mutate the jobs timestamps and user in the jobstatus resolver
* Request a token to mutate data

0.1.0 [03/11/2020]
******************

Added
-----

* Web service prototype to handle client requests to store/retrieve simulation data (#1)
* Use `GraphQL <https://graphql.org/>`_ query languages for the API (#1)
* Use `Tartiflette <https://github.com/tartiflette/tartiflette#tartiflette-over-http>`_ Python GraphQL server implementation (#1)
* Use `MongoDB <https://www.mongodb.com/>`_ as database (#1)
