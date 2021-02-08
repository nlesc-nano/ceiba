---
title: 'Ceiba: A web service to handle scientific simulation data'
tags:
  - Python
  - graphql
  - scientific simulations
  - computational chemistry
authors:
  - name: Felipe Zapata
    orcid: 0000-0001-8286-677X
    affiliation: 1
affiliations:
 - name: Netherlands eScience Center
   index: 1

date: February 2021
bibliography: paper.bib
---

# Summary
Efficient data handling is central in scientific research. The *Ceiba* library implements
a web service to perform data handling tasks like computing, storing and retreiving scientific simulation data
to/from a (remote) database.
Using  the *Ceiba-CLI* command line user can interact with the web service, they can for instance download available
data, upload data, request metadata, etc.

The *Ceiba web service* installation and deployment is intendent to be perform at a local/national infrastucture.
While the *Ceiba-CLI* can be easily install on personal computers, workstations or the supercomputer infrasctuctures
where the simulations are performed.

Ceiba is implemented in Python using the Tartiflete GraphQL [@graphql;@tartiflette] server.

# Statement of need
Scientific simulations generate large volume of data that needs to be stored and processed
by multidisciplinary teams across different geographical locations. Distributing
computational expensive simulations among the available resources, avoiding duplication
and keeping the data safe are challenges that scientists face every day.

Ceiba and its command line interface Ceiba-cli solve the problem of computing,
storing and securely sharing computationally expensive simulation results. Researchers
can save significant time and resources by easily computing new data and reusing existing
simulation data to answer their questions.


# Functionalities
Figure \ref{fig:architecture} represents schematically the architecture of the web service.
The *Ceiba-CLI* initializes the communication with the *Ceiba web service* by requesting some resources
(e.g. precomputed data). Then, the services checks that the requests is available and the user can
perform the action, if those initial steps success the service communicates with the database and
return the requested resources or performed the actions requested by the user.

![Diagram representing the Ceiba architecture.\label{fig:architecture}](architecture.jpg){ width=90% }

*Ceiba* Uses MongoDB [@mongodb] as backing database. Using a non-SQL database as MongoDB helps to
manipulate non-structure data, like json files, without having to impose a schema over the simulation data.

Currently the Ceiba library is focused on computational-chemistry/materials science but
it can be extended to other simulations domains.

# Examples
Let us suppose for the sake of the example that the web service URL is **http://ceiba.org:8080/graphql** (the actual
address depends on the actual hosting place). A user can then login into the web service by running the following command:
```bash
ceibacli login -t ${LOGIN_TOKEN} -w https://ceiba.org:8080/graphql
```
where `LOGIN_TOKEN` is is a [GitHub token to authenticate the user](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).

Once the user has been succesfully authenticated with the web service, she can request some available data like:
```bash
 ceibacli query -w http://localhost:8080/graphql
```
the web service response is:
```
Available collections:
	name size
	simulation1 23
	simulation2 5
```
The previous output means that there are two datasets: *simulation1* and *simulation2*, with 23 and 5 elements, respectively.
The Use can then request for all the available data in *simulation2* using the following command:
```bash
 ceibacli query -w http://localhost:8080/graphql --collection_name simulation2
```
After the command line returns, there should be a `simulation2.csv` file containing the dataset.

For a more comprenhensive discussion about how to interact with the web service, see the [Ceiba-CLI documentation](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).


# Acknowledgements
I would like to express my deepest appreciation to Stefan Verhoeven (@sverhoeven) for guiding me on the web developing world.
I am also grateful to Jen Wehner (@JensWehner) and Nicolas Renaud (@NicoRenaud) for their support and feedback designing 
the Ceiba web service.
