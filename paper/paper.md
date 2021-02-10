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
Efficient data handling is central in scientific research, but scientists do not usually follow best
practices for scientific computing and data management [@Wilson2017]. Data loss, unreproducible
results, inefficient resources usage, etc. are common consequences of not following best practices for
data and software.

The *Ceiba* web service aims to solve some of the aforementioned drawbacks by providing a interface to
perform data handling tasks like storing and retrieving scientific simulation data
to/from a (remote) database, using  the *Ceiba-CLI* command line interface.

A typical use case for the *Ceiba* web service is a large number of simulations that are performed as
independent jobs. For instance, a job can be a single molecular simulation under some specific conditions.
We would like to make all these jobs available to users, in such a way that they can run one or more jobs
at a time but avoiding that the same job is run by more than one user. Once the simulation is done,
a user can send the results to the web service or ask for already available results. We also want
to be able to call the web service from our local computer, specialized infrastructure or wherever
we want to perform the computation, without worrying about where the web service is running.

*Ceiba* is implemented in Python using the Tartiflete GraphQL server [@graphql;@tartiflette]. Finally,
the *Ceiba web service* installation and deployment is intendent to be performed at a local/national or
cloud computing infrastructure.


# Statement of need
Scientific simulations generate a large volume of data that needs to be stored and processed
by multidisciplinary teams across different geographical locations. Distributing
computational expensive simulations among the available resources, avoiding duplication,
and keeping the data safe are challenges that scientists face every day.

Ceiba and its command line interface Ceiba-cli solve the problem of computing,
storing and securely sharing computationally expensive simulation results. Researchers
can save considerable time and resources by easily computing new data and reusing existing
simulation data to answer their questions.


# Functionalities
Figure \ref{fig:architecture} represents schematically the architecture of the web service.
The *Ceiba-CLI* initializes the communication with the *Ceiba web service* by requesting some resources, for instance
some precomputed data or a new job to run. Then, the service checks that the requests is available and the user can
perform the action. Subsequently, if the initial step succeeds the service communicates with the database and
returns the requested resources and/or performs an update in the database.

![Diagram representing the Ceiba architecture.\label{fig:architecture}](architecture.jpg){ width=90% }

*Ceiba* Uses MongoDB [@mongodb] as backing database. Using a non-SQL database as MongoDB helps to
manipulate non-structure data, like json files, without having to impose a schema over the simulation data.

Currently the Ceiba library is focused on computational-chemistry/materials science but
it can be extended to other scientific fields.

# Examples
Let us suppose for the sake of the example that the web service URL is **https://ceiba.org:8080/graphql** (the actual
address depends on the domain/IP where you are hosting the service). A user can then login into the web service by running the following command:
```bash
ceibacli login -t ${LOGIN_TOKEN} -w https://ceiba.org:8080/graphql
```
where `LOGIN_TOKEN` is is a [read-only GitHub token to authenticate the user](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).

Once the user has been succesfully authenticated with the web service, she can request some available data like:
```bash
 ceibacli query -w http://localhost:8080/graphql
```
the web service response could be something like:
```
Available collections:
  name size
simulation1 23
simulation2 5
```
The previous output means that there are two datasets: *simulation1* and *simulation2*, with 23 and 5 elements, respectively.
The user can then request for all the available data in *simulation2* using the following command:
```bash
 ceibacli query -w http://localhost:8080/graphql --collection_name simulation2
```
After the command line returns, there should be a `simulation2.csv` file containing the dataset.

For a more comprehensive discussion about how to interact with the web service, see the [Ceiba-CLI documentation](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).


# Acknowledgements
I would like to express my deep gratitude to Stefan Verhoeven (@sverhoeven) for guiding me on the web developing world.
I am also grateful to Jen Wehner (@JensWehner), Nicolas Renaud (@NicoRenaud) and Pablo Lopez-Tarifa (@lopeztarifa)
for their support and feedback designing the Ceiba web service.
