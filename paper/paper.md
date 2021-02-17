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

Safe and efficient handling of large and complex data has become a critical part of many research projects. In particular, many datasets containing the results of computationally expensive simulations are being assembled in different scientific fields ranging from biology to material science. However,
many research teams lack the proper tools to collaboratively create, store and access datasets that are crucial for their research [@Wilson2017]. This lack of suitable
digital infrastructure can lead data loss, unreproducible results, and inefficient resources usage that hinders scientific progress. The *Ceiba* web service provides a technical solution for teams of researchers to jointly run the simulations needed to create their dataset, organize the data and the associated metadata and immediately share the datasets with each other. By doing so, *Ceiba* has the potential to not only improves the data handling practices in academic research but could also promote collaboration between independent research teams that requires the same data to perform their research.


A typical use case for the *Ceiba* web service is a large number of simulations that are performed as
independent jobs. For instance, a job can be a single molecular simulation under some specific conditions.
We would like to make all these jobs available to users, in such a way that they can run one or more jobs
at a time but avoiding that the same job is run by more than one user. Once the simulation is done,
a user can send the results to the web service or ask for already available results. We also want
to be able to call the web service from our local computer, specialized infrastructure or wherever
we want to perform the computation, without worrying about where the web service is running.


# Statement of need

*Ceiba* is implemented in Python using the Tartiflete GraphQL server [@graphql;@tartiflette]. *Ceiba* orchestrates the interaction 
between 3 distincts components : the client, the server and the database. Figure \ref{fig:architecture} represents schematically the architecture of the web service. 

**HOW DO WE CREATE THE DATABASE** 
**Where is the database stored**
**definition of the jobs etc ...**
*Ceiba* Uses MongoDB [@mongodb] as backing database. Using a non-SQL database as MongoDB helps to
manipulate non-structure data, like json files, without having to impose a schema over the simulation data.

The *Ceiba web service*  (*Ceiba-server*) should be installated and deployed at a local/national or cloud computing infrastructure. The server allows to handle client request, validate the request against a schema, connect to the database and return the data to the client. **Need to write that a bit better.**

After authentication (`Login`), users can request through the command line interface specifications of new jobs to compute new data points (`Compute`). This will return job files that users must execute either locally or on the ressources of their choice (cluster/cloud etc...).  Once the calculation complete, users can easily upload the results of these calculations in the central database (`Add`, `Report`). Users can also simply retrieve datapoints from the data base (`query`). 


![Diagram representing the Ceiba architecture.\label{fig:architecture}](architecture.jpg){ width=90% }


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
