# Data Space Concepts and Biodiversity Meets Data 

## Purpose of this document

In order to support the first iteration of the BMD data space (a minimal viable product), this document provides a concise overview of concepts coming from different initiatives working on European data spaces. Although there is no single definition or universally agreed implementation of a “data space”, there is emerging consensus around core ideas, roles, and building blocks.

This document draws on:

* [Data Space Support Center Glossary](https://dssc.eu/space/BVE2/1071251749/Glossary)
* [Data Spaces Blueprint v1.5](https://dssc.eu/space/bv15e/766061169/Data+Spaces+Blueprint+v1.5+-+Home)
* Green Deal Data Space (GDDS) concepts from AD4GD D1.4 — [Zenodo](https://doi.org/10.5281/zenodo.17200217)
* AD4GD D4.3 — Connecting the Green Deal Data Space — [Zenodo](https://doi.org/10.5281/zenodo.17200728)

In addition, documentation and protocols are emerging from the International Data Spaces Association [(IDSA)](https://docs.internationaldataspaces.org/ids-knowledgebase/dataspace-protocol). Many of ideas from IDSA are reflected and reused in the reports mentioned above.

---

## What is a Data Space?

A data space is an infrastructure that enables organisations to share and exchange  data in a trusted, controlled way. Unlike traditional data lakes where all data is  pooled in one place, data spaces allow data to remain with its provider while being discoverable and accessible through common standards and goverance framework.

The DSSC glossary defines it as:

> "Interoperable framework, based on common governance principles, standards, 
> practices and enabling services, that enables trusted data transactions 
> between participants."

Key principles for BMD:
- **Federated**: Data stays with providers (GBIF, EEA, CHELSA)
- **Standards-based**: Common APIs and metadata schemas enable interoperability
- **Governed**: Clear rules about who can access what, under which conditions
- **Modular**: Built from components that can be implemented incrementally


Another current initiative closely aligned with the Green Deal vision is SAGE [https://www.greendealdata.eu/](https://www.greendealdata.eu/)

---

## Scope for BMD MVP

For BMD, we focus on a few essential concepts that support the first milestone and can evolve over time.

---

## Building Blocks

### Participants

Organisations in a data space take on specific roles that determine their  responsibilities and what they can do. 

**Key roles envisioned in BMD:**

**Data Provider** — Organisation making data available
- Example: EEA provides Natura 2000 data 
- Responsibility: Maintain data quality, updating data, declare licensing terms

**Data Consumer** — Entities using data
- Example: A user using the BMD VRE for SDM analysis
- Responsibility: Comply with usage terms, cite sources

**Service Provider** — Organisation offering services
- Example: LifeWatch ERIC providing the visualization engine. Naturalis providing the data space. 
- Responsibility: Ensure service availability and performance

**Data Space Governance Authority** — Organisation setting policies
- Example: Naturalis coordinating BMD data space rules
- Responsibility: Define access policies, 

**Note**: Organisations can have multiple roles simultaneously.

---

### Data Products


In BMD, "data products" refers to curated, documented datasets with clear provenance and purpose. 

 A data product includes not just the data, but:
- Persistent identifier (PID: DOI or Handle)
- Comprehensive metadata (what, who, when, how)
- Processing lineage (source datasets → transformations → output)
- If possible: Quality indicators and known limitations
- Licensing and usage restrictions
- Dependencies on other data products or services

**BMD Examples:**

1. **GBIF-CHELSA Occurrence Cube** 
   - Input: GBIF occurrence records + CHELSA climate layers
   - Processing: Spatiotemporal harmonization at 1km² resolution
   - Output: Multi-dimensional datacube stored
   - Metadata: Includes species list, temporal range, climate variables
   
2. **SDM Results** (VRE)
   - Input: Occurrence cube + Natura 2000 boundaries
   - Processing: Hierarchical SDM workflow
   - Output: Distribution maps with uncertainty estimates
   - Metadata: Model parameters, validation metrics, projection scenarios

---

### Services

Services are capabilities offered within the data space. In BMD, services are essential for processing datasets, data cubes and delivering results to users.

**BMD Service Types Examples:**

1. **Data Access Services** (T4.1 - Data Integration Layer)
   - REST APIs for querying data cubes
   - Spatiotemporal filtering and subsetting
   - Format conversion (GeoJSON, NetCDF, Zarr etc )

2. **Computational Services** (T4.2 - Cloud Computing for VREs)
   - On-demand compute resource provisioning
   - Workflow orchestration 

3. **Visualization Services** (T4.3 - Data/Map Visualization Engine)
   - Web-GIS for exploring data cubes
   - Interactive map layers (WMS, WMTS)
   - Chart generation 

4. **Workflow Services** (WP5, supported by T4.1 Data Processing Layer)
   - FAIR workflow execution
   - Provenance capture via RO-Crate
   - Result publication back to data space

Services can be described using standardized metadata (DCAT, OpenAPI) allowing both humans and machines to find and use them.


---

### Governance Frameworks

Governance determines the "rules of engagement" for the data space: who can  access what, under which conditions, and with what obligations.

**BMD Governance Components:**

**1. Access Control** 
- If needed: User authentication via institutional login
- Role-based access (public data vs restricted species data)
- API keys for programmatic access

**2. Usage Policies** 
- Data licensing (CC-BY, CC0, custom restrictions)
- Citation requirements
- Allowed/prohibited use cases
- Sensitive species data handling 

**3. Data Agreements** (ODRL policies/open data contracts in metadata)
- Machine-readable data contracts
- Service Level Agreements

**4. Integration Governance** 
- Alignment with GDDS governance framework and EOSC policies 

**Practical Example**: 
A user wants to use occurrence data for an invasive species but these are listed as 
protected. The data space can check if user is authenticated and authorized. and if purpose matches allowed uses ("research and policy analysis"). 

Conceptually, there are two "planes": 

* **Data plane** — movement and processing of data
* **Control plane** — trust, identity, authorization, policy, discovery (driven by metadata)

Metadata mainly lives in the control plane but influences the data plane.

---

### Mapping to BMD MVP

* **GBIF** → Data Provider, Service Provider, partial Governance role
* **Naturalis** → Service Provider, Governance node
* **Data Cubes** → Data Products
* **VREs** → Value-added services and tools
* **BMD Data Space** → Federated domain data space connected to Green Deal / EOSC

### A practical MVP scenario

We have:

* a prototype data cube built from GBIF + CHELSA data
* Natura 2000 datasets accessed via EEA APIs or cached locally
* provenance, links, and licenses retained as metadata 

Example use case:

> *Assess the distribution of terrestrial invasive species (current and future) for species of Union concern.*

This requires **occurrence data** (GBIF records, supporting nested SDM workflows) and 
**predictor data** (CHELSA bioclimatic variables and other environmental layers).

There are specific **methods** which depends on the use case for example: Hierarchical SDMs, occupancy models, and climate-based projections.

And these produce certain **outputs** such as: 

* distribution maps
* risk indicators
* trends per site or Member State

All outputs should be registered also as **data products** with proper metadata. This also aligns with FAIR principles. 

---

### JSON example — Participants / Provider / Dataset (IDSA-inspired + GDDS concepts)

This is intentionally simple and conceptual for MVP discussions.
Also see emerging (open data product standard)[https://bitol-io.github.io/open-data-product-standard/latest/#example_1]


```json
{
  "@type": "dcat:Dataset",
  "@id": "https://bmd.eu/datasets/invasive-occurrence-cube-v1",
  "title": "BMD Invasive Species Occurrence Data Cube",
  "publisher": "Naturalis Biodiversity Center",
  "description": "Occurrence and predictor cube...",
  "license": "CC-BY-4.0",
  "accessURL": "https://api.bmd.eu/cubes/invasive-occurrence",
  "issued": "2026-01-10",
  "spatial": "European Union",
  "temporal": "2000-2025"
}
```

*Full technical schemas will be developed during T4.1 implementation based on GDDS recommendations.*

```
