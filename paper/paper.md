---
title: 'Ceiba: A web service to handle scientific simulation data'
tags:
  - Python
  - web service
  - scientific simulations
  - computational chemistry
authors:
  - name: Felipe Zapata
    orcid: 0000-0001-8286-677X
    affiliation: 1
  - name: Nicolas Renaud
    orcid: 0000-0001-9589-2694
	affiliation: 1
affiliations:
 - name: Netherlands eScience Center
   index: 1

date: February 2021
bibliography: paper.bib
---

# Summary

Safe and efficient handling of large and complex data has become a critical part of many research projects.
In particular, many datasets containing the results of computationally expensive simulations are being assembled
in different scientific fields ranging from biology to material science. However, many research teams lack the proper
tools to collaboratively create, store and access datasets that are crucial for their research [@Wilson2017].
This lack of suitable digital infrastructure can lead data loss, unreproducible results, and inefficient resources
usage that hinders scientific progress. The *Ceiba* web service provides a technical solution for teams of researchers
to jointly run the simulations needed to create their dataset, organize the data and the associated metadata and
immediately share the datasets with each other. By doing so, *Ceiba* has the potential to not only improves the data
handling practices in academic research but could also promote collaboration between independent research teams that
requires the same data to perform their research.

# Statement of need

Many resarch projects require running a large number of computationally heavy but independent simulations.
Those can be molecular dynamics simulations of proteins, fluid dynamics simulations with different initial conditions, etc.
As the number of independent simulations grows, their orchestration and execution require a collaborative effort among a
team of researchers. Through its dedicated server and command line interface, *Ceiba* facilitates this team effort.
*Ceiba* is implemented in Python using the Tartiflete GraphQL server [@graphql;@tartiflette].
*Ceiba* orchestrates the interaction between 3 distincts components: the client, the server and the database.
Figure \ref{fig:architecture} represents schematically the architecture of the web service. 

The *Ceiba web service* has been designed as a two levels service: one for managing the jobs generating
the data and another for handling the actual data. This partition, allow to keep a clean boundary between
the metadata and provenance of a given job, from the concrete results that produces that job. Since these
two layers are independent, Ceiba users can also manage data without associated jobs, for example, because
the data has been previously computed and users just want to share it among themselves.

We use docker [@docker] to setup and run both the server and the database in their own isolated and indepedent
linux containers. The server and database containers are deployed using docker-compose [@dockercompose] and
communicate with each other using their own internal network [@dockernetwork]. The docker-compose tool makes sure that
the server is listening to client requests in a given port (e.g. 8080 by default) and the database is stored
on the host computer where the docker containers are running, so it can be periodically backed up.
*Ceiba* Uses MongoDB [@mongodb] as backing database. Using a non-SQL database as MongoDB helps to
manipulate non-structure data, like json files, without having to impose a schema over the simulation data.

Since both the server and the database need some computational resources to run, we anticipate that both
the server and database can be deployed at a local/national or cloud computing infrastructure. 
Once the server is up and running, user can install the client (*ceiba-cli*) on their local computer,
national computing infrascture, cloud, etc. 

Using the client (*ceiba-cli*) the user can interact with the server and perform actions like:
 * store new jobs in the database
 * request some jobs to compute
 * report the jobs' results
 * query some available data
 * perform administrative tasks on the database

Notice that in order to keep the data safe, it is required that users login with the Ceiba web service.
Since managing our own authentication system takes considerable time and resources, we use the
GitHub authentication system [@authentication] to authenticate users on behalf of the Ceiba Web service. Users just
need to have a GitHub account and request a personal access token [@token].

Once the user has authenticated with the web service, she can add new jobs by calling the client (`ceibacli add`)
with a YAML input file specifying the parameters to run the simulation. Similarly, the user can request through
the command line interface the parameters to compute new data points (`ceibacli compute`). This last command,
will fetch the parameters to run a specific calculation and will feed those parameters to the executable
provided by the user, as part of the input for `compute` command. Finally, the client will run the job locally
or on the ressources specified by the user (cluster/cloud etc.). Notice that when a user request to compute a job,
that job is not longer available for other users and will remain in a "reserved" state until its corresponding
results are reported or a given amount of time has passed without receiving the results. This reservation mechanism
ensures that two users do not compute the same datapoint, saving computational ressources and human time.

Having run the jobs, the user can easily upload (`ceibacli report`) the results and their metadata in
the central database. Also, at all times the user can retrieve available datapoints from the database 
(`ceibacli query`). The example section will provide a hands-on ilustration of the aforementioned actions.


![Diagram representing the Ceiba architecture.\label{fig:architecture}](architecture.jpg){ width=90% }


# Examples

## Creation of the database

For this example we will consider a simple case where a database containing XXX must be computed by different collaborators.
Before using *Ceiba* the administrator of the database, Adam, must create the database. While in a real aplication this database
will most likely be stored on a cloud service, we will for the sake if illustration create a local dabase in a docker container.
Once the database create Adam must specify the jobs that his collaborators will run to compute the different data points.
*Example of how to do that*

## Requesting job and uploading the results

Now that the database is created, Julie a collaborator of Adam wants to request XX jobs to compute. She must first must login to the database 

```bash
ceibacli login -t ${LOGIN_TOKEN} -w https://ceiba.org:8080/graphql
```
where `LOGIN_TOKEN` is is a [read-only GitHub token to authenticate the user](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).
Once authentication is complete Julie can request job with :

```bash
ceibacli compute <....>
```

This return here available job files `xxx` that still needs to be computed. These jobs will now be markes as 'In progress' in the database so that other collaborators can't compute them as well. Julie can run locally those jobs to obtaing the results of the simulations that are then stored in file `xxxx`. Julie can then upload these new datapoints to the central database by executing 

```bash
ceibacli report <......>
```
The jobs run by Julie will now be marked as `Completed` in the database. Julie or other collaborators can keep on requesting new jobs to compute through the `ceilacli compute` command and report those results via `ceibacli report`. 

## Querying the database

At any point all the collaborators can obtain an overview of the current status in the database via :  

```bash
 ceibacli query -w http://localhost:8080/graphql
```

This will return :

```
Available collections:
  name size
simulation1 23
simulation2 5
```

indicating that there are currently two datasets: *simulation1* and *simulation2*, with 23 and 5 elements, respectively.

If user want to retreive all the available data in *simulation2* they can use:
```bash
 ceibacli query -w http://localhost:8080/graphql --collection_name simulation2
```
that will create a `simulation2.csv` file containing the dataset.

For a more comprehensive discussion about how to interact with the web service, see the [Ceiba-CLI documentation](https://ceiba-cli.readthedocs.io/en/latest/authentication.html#authentication).


# Acknowledgements
Felipe would like to express his deepest gratitude to Stefan Verhoeven (@sverhoeven) for guiding him on the web developing world.
We are also grateful to Jen Wehner (@JensWehner) and Pablo Lopez-Tarifa (@lopeztarifa)
for their support and feedback designing the Ceiba web service.
