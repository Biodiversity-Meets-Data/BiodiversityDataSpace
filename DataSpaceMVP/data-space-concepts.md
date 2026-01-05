In order to faciliate the work of the First version of data space delivered by the BMD project, this document provides summary and exmaple based on 

- Data Spaces Blueprint version 2.0 https://dssc.eu/space/bv15e/766061169/Data+Spaces+Blueprint+v1.5+-+Home
- Green Deal data space concepts deliverable from All Data 4 Green Deal AD4GD D4.3 Connecting the Green Deal Data Space (final). Zenodo.
https://doi.org/10.5281/zenodo.17200728

https://zenodo.org/records/17200728 (AD4GD D4.3 Connecting the Green Deal Data Space (final)) 

According to the Data Spaces Support Centre (DSSC) and International Data Spaces Association (IDSA), data spaces consist of modular building blocks that can be implemented and combined.



# Building blocks for MVP 


## Participants

GDDS blueprint and concept clarifies that metadata supports different views depending on the participant:

- Providers can describe availability, terms, lineage
- Consumers understand appropriateness, licenses, risks
- Governance actors understand compliance and accountability
- governance arrangements are captured and expressed through metadata and policy models

Few examples: 

EEA - Provides Natura 2000 protected area data
GBIF - Provides species occurrence records
CHELSA - Provides climate data layers

## Data Products 

"data cubes" using GBIF and CHELSA data, derived SDMs are all data products.

Metadata must capture: Product identity (PID, version), offernings /value provided, Dependencies (what inputs were used), Processing steps, Quality indicators
Responsible organisation, Usage constraints

The idea is ot support traceability of data products, enabling reproducibility, accountability, and reuse across contexts. 

## Services 

In GDDS, services (for example these could be APIs, computation, AI pipelines, model workflows) are also described through metadata so that they can be:

discovered, composed, governed and monitored

Services and workflows are represented alongside datasets enabling composibility and automation

## Governance Frameworks

GDDS metadata explicitly encodes governance concepts:

- who may access what
- under what conditions
- contractual terms / license
- obligations of reuse
- ethical or legal  constraints (FAIR and CARE) 
- logging and audit


Data plane: actual movement/query of data
Control plane: trust, identity, authorization, policy, discovery driven by metadata

Metadata lives primarily in the control plane, but influences behavior in the data plane.


In GDDS language:

GBIF = Data Provider, Service Provider, and partial Governance node
Naturalis = Service Provider and Governance node
Data Cubes = Data Products
VREs = Value-added processing services and tools 
BMD Data Space = federated domain data space connected to Green Deal / EOSC 


Green Deal Information Model (GDIM)-aligned metadata. rich enough to support interoperability, provenance, governance, and machine actionability in a Green Deal Data Space context, and

Open Data Product Standard (ODPS)-style YAML — a growing open standard for defining data products (includes input/output ports, contracts, governance, and custom metadata)
