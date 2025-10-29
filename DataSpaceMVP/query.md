This describes some of the initial ideas behind the first version of the data space. 

We need to understand how to capture the query. The query schema/framework can be thought of as the entry point. 
Then FAIR and Data Space compoments come in. What happens after the query. How we store, describe, and connect the different artefacts (cubes, datasets, results etc). This is where RO-Crate, sementics, and Triplestore will come into play. 


The query schema is the entry point, but the real FAIR and Data Space power comes from what happens after the query — how you store, describe, and connect the resulting artefacts (queries, cubes, datasets) via RO-Crates, semantic metadata, and your TripleStore.




| Component                           | Role in the BMD Data Space                                                                                                                                                 
| ----------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| **RO-Crate**                        | FAIR packaging format to encapsulate the workflow, query, input data, process, and result (cube, visualisation).            |  
| **Semantic metadata (RDF/JSON-LD)** | The data model that gives machine-actionable meaning to the RO-Crate contents (e.g., DwC, DCAT, PROV). |  
| **TripleStore (RDF store)**   | The internal database that stores and links all semantic entities (species, sites, datasets, queries, provenance).  |             |



We are also trying to align with Darwin Core Data Package ideas (https://gbif.github.io/dwc-dp/dp/), Data Space concepts (participants, usage policies, provenance).
and also with the awareness of EUNIS / Natura 2000 data models. 

BMD WP3 and WP5 tasks are also proceeding with data cube and VRE work. 

A core design idea is to keep a metadata layer within the data space (that sits between the query interface/VRE and the data cube store).

This layer might need key crosswalk table such as this to connect species taxon id with site code etc. 


| Entity              | Main identifier                     | Crosslinks                                                                       |
| ------------------- | ----------------------------------- | -------------------------------------------------------------------------------- |
| **Species / Taxon** | `taxonID` (CoL URI or GBIF key)     | EUNIS ID, Habitats/Birds Directive code (`code_2000`), group name, taxonomy tree |
| **Habitat**         | EUNIS habitat code                  | Annex I code (Habitats Directive)                                                |
| **Site**            | Natura 2000 site code (`code_site`) | EUNIS site ID, spatial footprint, member state                                   |

Example data from EUNIS (from https://discodata.eea.europa.eu/Help.html) 

```
{
        "id_eunis": 1098,
        "code_2000": "A338",
        "scientific_name": "Lanius collurio",
        "author": "Linnaeus, 1758",
        "is_accepted_name": 1,
        "status_name": "Accepted name",
        "taxonomy_level_name": "Species",
        "species_group_name": "Birds",
        "taxonomy_tree": "46*Kingdom*Animalia,4821*Phylum*Chordata,1691*Class*Aves,851*Order*Passeriformes,856*Family*Laniidae,284479*Genus*Lanius,423502*Species*Lanius collurio",
        "id_eunis_accepted": 1098,
        "code2000_accepted": "A338",
        "scientific_name_accepted": "Lanius collurio",
        "author_accepted": "Linnaeus, 1758",
        "col_dataset": "9854",
        "col_id": "3S7BJ"
    }
```

site-species data 
```
{
        "code_site": "AT1110137",
        "id_eunis": 1098,
        "code_2000": "A338",
        "species_name": "Lanius collurio",
        "species_group_name": "Birds",
        "picture_url": "https://eunis.eea.europa.eu/images/species/1098/thumbnail.jpg"
    },
    {
        "code_site": "AT1119622",
        "id_eunis": 1098,
        "code_2000": "A338",
        "species_name": "Lanius collurio",
        "species_group_name": "Birds",
        "picture_url": "https://eunis.eea.europa.eu/images/species/1098/thumbnail.jpg"
    },
    {
        "code_site": "AT1125129",
        "id_eunis": 1098,
        "code_2000": "A338",
        "species_name": "Lanius collurio",
        "species_group_name": "Birds",
        "picture_url": "https://eunis.eea.europa.eu/images/species/1098/thumbnail.jpg"
    },
```

When a query mentions a species or site, the query parser looks up this metadata table to:

find the CoL ID, EUNIS ID, and Habitat Directive code;
resolve spatial extent via the Natura 2000 site geometry;
enrich the query before matching it to cubes.

But the query might not specify a Natura 2000 site or EUNIS code, but can specity a geographic area defined by:

a country, a named locality or region, or a geometry file (e.g., shapefile, GeoJSON, WKT).

So we should make sure the query JSON supports both:

semantic filters (e.g., Natura2000 site, species, directive), and 
spatial filters (country, locality, polygon).

The query parser can decide precedence:
if geometry the use it directly;
else if site then resolve via metadata catalogue;
else if locality or countryCode then use country boundaries. etc. This will also depend on stakeholder feedback. 

This is one way to strcuture the query with FAIR, data space, and semantic JSON-LD in mind: 

```
Query
├── Context & Semantics (JSON-LD)
├── Consumer & Authentication (if needed) 
├── Core Question
│   ├── Taxon (Darwin Core + EUNIS)
│   ├── Spatial (Natura2000 sites + geometry)
│   ├── Temporal (range + resolution)
│   └── Theme (occurrence/modelled/etc.)
├── Analysis Specification
│   ├── Indicator (population_trend)
│   ├── Method (TRIM, state-space)
│   └── Parameters
├── Output Requirements
│   ├── Format (NetCDF, GeoJSON)
│   ├── Visualizations
│   └── Delivery endpoint
├── Data Provenance
├── Usage Policies
└── Service Information

```

We also need to think about the response structure:

```
{
  "@context": "...",
  "queryId": "urn:uuid:1234-5678-90ab-cdef",
  "status": "completed",
  "result": {
    "dataCube": "https://data.bmd.eu/cubes/trend-12345.nc",
    "visualisations": {
      "timeSeries": "https://viz.bmd.eu/ts/12345",
      "trendMap": "https://viz.bmd.eu/map/12345"
    },
    "metadata": {
      "computationDate": "2025-10-28T14:30:00Z",
      "sourcesUsed": ["GBIF", "EEA"]
    }
  }
}
```

Query example: https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/DataSpaceMVP/bmd-query-example.json


