# Purpose of this document

In order to support the first iteration of the BMD data space (a minimal viable product), this document provides a concise overview of concepts coming from different initiatives working on European data spaces. Although there is no single definition or universally agreed implementation of a “data space”, there is emerging consensus around core ideas, roles, and building blocks.

This document draws on:

* [Data Space Support Center Glossary](https://dssc.eu/space/BVE2/1071251749/Glossary)
* [Data Spaces Blueprint v1.5](https://dssc.eu/space/bv15e/766061169/Data+Spaces+Blueprint+v1.5+-+Home)
* Green Deal Data Space (GDDS) concepts from AD4GD D1.4 — [Zenodo](https://doi.org/10.5281/zenodo.17200217)
* AD4GD D4.3 — Connecting the Green Deal Data Space — [Zenodo](https://doi.org/10.5281/zenodo.17200728)

In addition, documentation and protocols are emerging from the International Data Spaces Association (IDSA):[https://docs.internationaldataspaces.org/ids-knowledgebase/dataspace-protocol](https://docs.internationaldataspaces.org/ids-knowledgebase/dataspace-protocol)

Many of ideas from IDSA are reflected and reused in the reports mentioned above.

---

## What is a Data Space?

The DSSC glossary (adopted from the CEN Workshop Agreement on Trusted Data Transactions) describes a data space as:

> **Interoperable framework, based on common governance principles, standards, practices and enabling services, that enables trusted data transactions between participants.**

Another shared principle is that data spaces are **modular** that means they are composed of building blocks that can be implemented independently and combined over time.

Another current initiative closely aligned with the Green Deal vision is SAGE:

> [https://www.greendealdata.eu/](https://www.greendealdata.eu/)
> “The SAGE (Sustainable Green Europe Data Space) project will develop a federated, secure, and interoperable data space to support the European Green Deal…”

---

## Scope for BMD MVP

For BMD, we focus on a few essential concepts that support the first milestone and can evolve over time.

---

## Building Blocks

### Participants

Participants in a data space can take on different roles.
It is therefore important to record **who they are** and **what they do** via metadata.

Based on DSSC guidelines, the main roles are:

* **Data Provider** — entity providing data to the ecosystem
* **Data Consumer** — entity using or receiving data
* **Data Space Governance Authority** — entity defining and enforcing data space rules
* **Service Provider** — entity offering services (catalogues, APIs, computation, etc.)

Examples in the BMD context

* **EEA** — provides Natura 2000 protected area data
* **GBIF** — provides species occurrence records
* **CHELSA** — provides climate predictor layers

In practice: (a few examples, not an exhaustive list)

* GBIF acts as **Data Provider**, **Service Provider**, and participate in governance discussions
* Naturalis acts as **Service Provider** and **Data Space Governance Authority**
* LifeWatch ERIC acts as **Service Provider**

---

### Data Products

Data products are not just “datasets”. They are packaged, documented resources with purpose and governance.

Examples in BMD:

* Data cubes using GBIF and CHELSA data 
* Derived SDM results
* Aggregated indicators per region or protected area

Metadata needs to capture:

* Product identity (PID, version)
* Value proposition (what the product enables)
* Dependencies (input datasets and services)
* Processing and transformation steps
* Quality indicators and uncertainty
* Responsible organisation
* Licensing and usage constraints

Goal is to enable traceability, reproducibility, accountability, and responsible reuse.

---

### Services

In data spaces, services are important components. They can be:

* APIs
* computational workflows
* AI pipelines
* modeling environments (e.g., VREs)

They are also described through metadata.

Datasets, services, and workflows can be also described **together**, enabling automation and interoperability.

---

### Governance Frameworks

GDDS concepts places governance inside metadata.

Key concepts include:

* who can access which resources
* under what conditions
* contracts and licenses
* obligations for reuse
* legal and ethical constraints (FAIR, CARE, etc.)
* logging and auditing requirements

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

It captures:

* participant identity
* role
* dataset (as data product)
* policy / governance hints
* provenance references

```json
{
  "@context": {
    "dcat": "https://www.w3.org/ns/dcat#",
    "dct": "http://purl.org/dc/terms/",
    "odrl": "http://www.w3.org/ns/odrl/2/",
    "dspace": "https://w3id.org/dspace/v1/",
    "xsd": "http://www.w3.org/2001/XMLSchema#"
  },
  "@type": "dcat:Catalog",
  "dspace:participantId": "urn:participant:naturalis",  
  "dcat:dataset": [
    {
      "@type": "dcat:Dataset",
      "@id": "urn:dataset:bmd:invasive-occurrence-cube-v1",
      "dct:title": "BMD Invasive Species Occurrence Data Cube",
      "dct:description": "Harmonized occurrence and predictor cube for EU invasive species modeling",
      "dct:publisher": {
        "name": "Naturalis Biodiversity Center",
        "id": "urn:participant:naturalis"
      },
      "odrl:hasPolicy": [
        {
          "@type": "odrl:Offer",
          "odrl:permission": [
            {
              "odrl:action": "odrl:read",
              "odrl:assignee": "urn:participant:*"
            }
          ],
          "odrl:constraint": [
            {
              "odrl:operator": "odrl:eq",
              "odrl:purpose": "research and policy analysis"
            }
          ]
        }
      ],
      "dcat:distribution": [
        {
          "@type": "dcat:Distribution",
          "dcat:accessURL": "https://dataspace.bmd.org/cubes/invasive-occurrence",
          "dcat:mediaType": "application/json",
          "dcat:dataService": {
            "@type": "dcat:DataService",
            "dcat:endpointURL": "https://connector.bmd.org/ids/api",
            "dspace:dataServiceType": "dspace:connector"
          }
        }
      ],
      "dct:issued": "2026-01-10T00:00:00Z",
      "dct:modified": "2026-01-10T00:00:00Z"
    }
  ]
}

```

