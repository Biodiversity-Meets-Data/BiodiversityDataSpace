# Example STAC metadata 

Here we describe some patterns for creating STAC Collections and Items aligned with FAIR and the Data Space concept. 

The main idea is this: 

STAC only describes *what the data is and where to get it* — governance (license, rights),
provenance (where it came from), and rich description (DCAT) are kept **outside** STAC and referenced through typed links. 

As part of our tests we need to decide whether to embed external metadata in the STAC JSON or 
to reference it via typed links; embedding makes Items heavier and requires versioning, while linking keeps Items lightweight.


This README is a quick guide to that pattern, and a few simple examples. 


This is still exploratory. We're testing what a STAC-based Data Product pattern looks like for this Data Space. 


## Why STAC, in a Data Space

A Data Space (per the [DSSC Blueprint](https://archive.dssc.eu/space/Glossary/176554052/2.+Core+Concepts))
is built from a handful of separable building blocks: 

- **Data, Services & Offerings Descriptions** (like DCAT), 
- **Publication & Discovery**, (like STAC)
- **Provenance & Traceability** (PROV-O), and 
- **Access & Usage Policies and Control** (ODRL). 

Each is its own standard. This is on purpose as data space is meant to
federate participants who each bring their own catalogues, so the pieces
have to stay decoupled rather than baked into one format.

STAC fits naturally into the *Data Description + Discovery* aspects here. It's already a machine-readable, geospatially-aware catalogue
format with a working ecosystem (clients, APIs, extensions) and can  plug into the other building blocks. 


## Examples in this repo

Three different ways to include the metadata. 


- **[`stac-data-space-bmd-example.json`](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/STAC-tests/examples/stac-data-space-bmd-example.json)**
  — a Collection showing  `describedby`
  → DCAT, a namespaced ODRL link rel, `cite-as` → DOI resolver alongside a
  `sci:doi` property from the `scientific` extension, and
  `producer`/`host`/`licensor` provider roles. 

- **[`stac-item-with-embedded-odrl-dataspaces.json`](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/STAC-tests/examples/stac-item-with-embedded-odrl-dataspaces.json)**
  — This show how embedding ODRL detail can be: the full ODRL policy (JSON-LD, `odrl:policy`) is 
  embedded directly inside `properties`, not linked. This can be part of further tests to to see  what
  embedding actually costs. The Item now has to carry, version, and keep
  in sync a whole external vocabulary's document instead of a pointer to
  one. 

- **[`stac-item-with-external-odrl-dataspaces.json`](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/STAC-tests/examples/stac-item-with-external-odrl-dataspaces.json)**
  — the Item stays clean and the ODRL document is external, but it's
  reached through a plain `rel: "license"` link rather than a
  namespaced ODRL relation. 
  

## The pattern

An STAC Item stays lightweight. Anything that isn't "what/where" is a pointer to
an external entity.

```mermaid
flowchart LR
  subgraph Catalog
    STAC_CATALOG["STAC Catalog\ncatalog.example.org"]
    STAC_ITEM["STAC Item\n(open metadata)\nid: dataset-8-2024-07-15\nlinks: rel=license -> https://policies.example.org/odrl/landsat-8-dataspace-policy.jsonld"]
    STAC_CATALOG --> STAC_ITEM
  end

  subgraph Assets
    ASSET["Asset (restricted payload)\nlandsat-8_B4.tif\nhref: https://data.example.org/landsat/2024/07/15/landsat-8_B4.tif"]
  end

  STAC_ITEM --> ASSET
  STAC_ITEM --> ODRL_LINK["link: policy (external JSON-LD)"]
  ODRL_LINK --> ODRL["ODRL Policy (external JSON-LD)\nhttps://policies.example.org/odrl/landsat-8-dataspace-policy.jsonld\nprofile: Data Spaces\npermission: action=display/use, purpose=research"]

  Client["User / Client"] -->|GET metadata| STAC_ITEM
  Client -->|request asset| ASSET
  ASSET -->|policy-check| ODRL
  ODRL -->|allow / deny| ASSET

  classDef stacFill fill:#e6f2ff,stroke:#6fa8dc;
  classDef assetFill fill:#ffe6e6,stroke:#e06666;
  classDef policyFill fill:#fff8d9,stroke:#f1c232;
  class STAC_CATALOG,STAC_ITEM stacFill;
  class ASSET assetFill;
  class ODRL policyFill;
```

Ideally, the item should not be overloaded with ODRL, DCAT, or PROV content. 
Same idea applies to provenance and attribution: the Item says *who
produced / provided the data* and *where it came from* via a `providers`
list and links. 



## Minimum metadata to check 

- **License** — a `license` link (or SPDX string) pointing to real license
  terms, not just an opaque file with no context.
- **Provider / producer** — who actually made the source data, distinct
  from whoever re-packaged it for this catalog.
- **Provenance** — a link back to the original dataset/service this Item
  was derived from, so a consumer can trace it upstream.

Operational fields (auth scheme, storage endpoint, checksums) can belong
directly on the Item, because Items are often fetched programmatically.

Governance and provenance can live on the Collection level and be reached via the Item's `collection`
link. 


## Example: `natura2000 data`

This Item reuses Natura 2000 site data originally produced by the
**European Environment Agency (EEA)**. 


```json
"providers": [
  { "name": "European Environment Agency", "roles": ["licensor", "producer"], "url": "https://www.eea.europa.eu/" },
  { "name": "<this catalog's operator>", "roles": ["processor", "host"] }
],
"links": [
  { "rel": "license", "href": "<real EEA/Natura2000 license terms URL>", "type": "text/html" },
  { "rel": "derived_from", "href": "<original EEA Natura2000 dataset URL>", "type": "text/html", "title": "Source dataset (EEA)" }
]
```

## Example: Checklistbank data 


This (https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/STAC-tests/examples/checklistbank-annex.json) is a simplified STAC Item example that describes a single Parquet table derived from a ChecklistBank dataset. The Item records basic provenance (who created, who published/licenced, who transformed/hosts) and includes an asset describing the Parquet file and its column layout.

### Provenance hop (EEA → ChecklistBank → BMD)
-------------------------------------------
- EEA (European Environment Agency)
  - Acts as the dataset creator / licensor in the source chain.
  - The EEA is acknowledged in links and providers so users know the licence and publisher.
- ChecklistBank
  - The source/producer of the taxonomic checklist (referenced via its dataset YAML URL).
  - Represented in providers as the original producer and included as a `derived_from` link.
- BMD Project
  - Processes/transforms the ChecklistBank tables into a Parquet file (this STAC Item).
  - Listed in providers as the processor/host and the `prov:generatedBy` block records the ETL script and version.

### How this is represented in the STAC Item
----------------------------------------
- providers: records ChecklistBank (producer), EEA (licensor/publisher), and BMD (processor/host).
- links:
  - `derived_from` → the ChecklistBank dataset YAML (source).
  - `license` → EEA licence URL (placeholder in the example; replace with the real URL or SPDX identifier).
- properties:
  - Small PROV-like fields (`prov:wasDerivedFrom`, `prov:generatedBy`, `prov:generatedAtTime`) for quick traceability.
  - `citation` / acknowledgement text for human-readable attribution.
- assets:
  - Single `table` asset with `type: application/vnd.apache.parquet`, `roles: ["data"]`.
  - Includes `table:row_count`, `file:size`, and `table:columns` (the column list you requested — preserved exactly).
  - These asset-level fields let tools decide which file to download and how to interpret it.


- Standardized metadata: STAC defines `providers`, `links`, `assets`, and `properties`, giving a common, machine-readable structure.
- Explicit links: `derived_from` and `license` links make the source and licence discoverable and machine-actionable.
- Asset-first model: Each data file is an asset with MIME type, roles, size, and optional checksums — ideal for datasets with many files or formats.
- Indexing & discovery: STAC catalogs/collections enable search by item properties (e.g., dataset id, datetime) and efficient harvesting by STAC APIs.
- Interoperability: STAC maps cleanly to other metadata standards (ISO/OGC, PROV, ODRL), so you can export or harvest into other catalogues.
- Lightweight provenance: Basic `prov:` fields or a PROV extension are sufficient for most users; stronger W3C-PROV or ODRL links can be added when needed.




## Reference

- STAC spec: link relations, provider roles, extensions —
  https://github.com/radiantearth/stac-spec
- `authentication`, `alternate-assets`, `scientific`, `file` extensions —
  https://stac-extensions.github.io/
