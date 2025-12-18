According to the Data Spaces Support Centre (DSSC) and International Data Spaces Association (IDSA), data spaces consist of modular building blocks that can be implemented and combined.

## Core Participants (Roles)

Every data space has these key roles:

- 1 Data Provider

Organizations that make data available to the data space.

In BMD (a few examples): 

EEA - Provides Natura 2000 protected area data
GBIF - Provides species occurrence records
CHELSA - Provides climate data layers

- 2 Data Consumer

Organizations or individuals that use data from the data space.

BMD stakeholders. 

- 3 Service Provider

Organisations that operate infrastructure and provide technical services.

In BMD: The organisations in the consortium that operates cloud storage, connectors, APIs, and catalog services


- 4  Data Space Authority (optional)
  
Organisation that governs the data space and maintains rules.

- 5  Intermediaries

Additional actors that facilitate data exchange (some of these can be maintained by same organisations that are also provider or consumers). 
 - Brokers/Catalogs - Make data discoverable (e.g., GeoNetwork)
- Identity Providers - Manage authentication and authorization

## Technical Building Blocks

Connectors: Software components that enable secure data exchange between participants.

BMD operates a connector that pulls data from EEA, GBIF, CHELSA for instance. 

Transforms and integrates data exposes unified APIs
Enforces attribution and license requirements



## Example 

| Role              | Organisation | Contribution |
| :---------------- | :------: | ----: |
|Data Providers      |   EEA   | |
|                   |  GBIF   |  |
|                   | CHELSA | |
| Service Provider| BMD consortium | Cloud infrastructure, data integration, API services |
| Data Consumers | BMD users | |
|Catalog| GeoNetwork| Metadata management and discovery|
