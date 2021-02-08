---
title: 'Ceiba: A web service to handle scientific simulation data'
tags:
  - Python
  - scientific simulations
  - graphql
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

Ceiba is implemented in Python using the Tartiflete GraphQL server.

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
![Diagram representing the Ceiba architecture.\label{fig:architecture}](architecture.jpg)


# Figures

Figures can be included like this:
![Caption for example figure.\label{fig:example}](figure.png)
and referenced from text using \autoref{fig:example}.

Figure sizes can be customized by adding an optional second parameter:
![Caption for example figure.](figure.png){ width=20% }

# Acknowledgements
I would like to express my deepest appreciation to Stefan Verhoeven (@sverhoeven) for guiding me on the web developing world.
I am also grateful to Jen Wehner (@JensWehner) and Nicolas Renaud (@NicoRenaud) for their support and feedback designing 
the Ceiba web service.
	
# References
