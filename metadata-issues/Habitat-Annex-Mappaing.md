# EEA Data Identifier and Metadata Harmonisation

A [user story collected from our stakeholders](https://github.com/Biodiversity-Meets-Data/WP1/issues/6) describes the need from a Natura 2000 site manager:

> *As a Natura 2000 site manager, I need to access timely data on habitat quality, species presence and abundance, and climate change scenarios — so that I can prioritise my restoration and conservation proposals, inform my decision-making and secure funding for biodiversity protection in the freshwater realm.*

This site manager needs to pull together habitat information for a specific set of sites and turn that into something actionable. They would start from a known site (for example [ES0000034](https://eunis.eea.europa.eu/sites/ES0000034)) 
and navigate to the designated habitat types and species for that site, then link other data. In current practice, this link breaks easily 
as there is no consistent way for habitat code and EUNIS classfication codes are used in related to the site code. For example, the Annex I habitat code appears with or without an `H` prefix depending on the tool, 
and the EUNIS crosswalk is distributed across classification versions with no single authoritative lookup. 
The result is that every project (including BMD) needs to rebuild these mappings from scratch, inconsistently. 

This document is a first attempt to record what we found, what tools exist, and the decisions the project needs to make so that the data pipeline serving this user actually works end to end.

For the SQL query and JSON examples, we used https://discodata.eea.europa.eu/Help.html. 

---

## The Identifiers 

### 1. Annex I Habitat Codes: 

The Habitats Directive assigns 4-character numeric codes to Annex I habitat types. In practice these appear in **at least four different formats**:

| Source / System | Format used | Example |
|---|---|---|
| EEA table — `code_2000` field | Bare numeric | `1220` |
| EEA table — `habitat_unique_id` field | `ANNEX1_` prefixed | `ANNEX1_1220` |
| EU Interpretation Manual (EUR28) | Bare numeric | `1220` |
| EEA viewer, many national databases, research tools | `H`-prefixed | `H1220` |
| `eunis.habitats` R package | Bare numeric | `1220` |

For example, querying `[EUNIS].[latest].[Habitat_Information]` for habitat code `3190` (Lakes of gypsum karst) returns:

JSON snippets: 

```json

 {
        "id_habitat": 10240,
        "scientific_name": "Lakes of gypsum karst",
        "scientific_name_clean": "Lakes of gypsum karst",
        "english_name": "Lakes of gypsum karst",
        "id_dc": 2435,
        "code_2000": "3190",
        "priority": 0,
        "eunis_habitat_code": "",
        "habitat_category": "ANNEX1",
        "habitat_unique_id": "ANNEX1_3190",
        "SEA_NAME": null,
        "habitat_type_tree": "ANNEX1_3$3 - FRESHWATER HABITATS|ANNEX1_3100$3100 - Standing water|ANNEX1_3190$3190 - Lakes of gypsum karst"
    }

```

The same habitat in another table ->  `[BISE].[latest].[Habitat_Information]`:

```json
{
    "code_2000": "3190",
    "habitat_category": "ANNEX1",
    "habitat_unique_id": "ANNEX1_3190",
    "number_countries": 4,
    "number_sites": 19
}
```

Both use `ANNEX1_3190` as the unique identifier which is good but the `eunis_habitat_code` field is empty. To get the EUNIS link you need look up a separate table. 

---

### 2. EUNIS–Annex I Crosswalk: Not embedded in the main habitat tables

As mentioned, the EUNIS link must be retrieved from a separate table. `[BISE].[latest].[Habitat_EUNIS_Classification]` does contain the crosswalk, but the relationship is hierarchical and requires interpretation. 
For example, habitat `1220`: (FYI "code_2000": "3190" is missing from this table) 

```json
[
    {"code_2000": "1220", "habitat_code": "B",   "scientific_name": "Coastal habitats",                          "level": 1},
    {"code_2000": "1220", "habitat_code": "B2",  "scientific_name": "Coastal shingle",                          "level": 2},
    {"code_2000": "1220", "habitat_code": "B2.3","scientific_name": "Upper shingle beaches with open vegetation","level": 3}
]
```

And for habitat `1520`:

```json
[
    {"code_2000": "1520", "habitat_code": "F",   "scientific_name": "Heathland and scrub",        "level": 1},
    {"code_2000": "1520", "habitat_code": "F6",  "scientific_name": "Garrigue",                   "level": 2},
    {"code_2000": "1520", "habitat_code": "F6.7","scientific_name": "Mediterranean gypsum scrubs","level": 3}
]
```

The rows represent a path through the EUNIS hierarchy. The details of this hierarch is probably documented somewhere else but not machine interpretable here. 


The target structure the BMD project can work towards is something like this: 

```json
{
  "annex1_code": "H1220",
  "name": "Perennial vegetation of stony banks",
  "priority": false,
  "eunis_primary": "B2.3",
  "eunis_components": ["B2.3", "B2.4", "B2.41", "B2.5", "B2.6"],
  "notes": "EUNIS parent: Coastal shingle"
}
```

This structure can accompany a [SSSOM](https://mapping-commons.github.io/sssom/)-style mapping file for interoperability.

---

These issues are not specific to BMD.



[A 2022 analysis of Natura 2000 species data](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC12451482/) found that member states frequently fail to follow EU reporting guidelines, 
resulting in heterogeneity across Standard Data Forms including typological and completion errors. 

[Thoonen et al. (2015)](https://www.sciencedirect.com/science/article/abs/pii/S0098300415300327) identified semantic heterogeneity as the barrier to Natura 2000 data comparability across member states.



## Available tools and data sources

### EEA Discomap SQL Viewer
Direct table exploration of the EEA's EUNIS/Natura 2000 database — useful for verifying linkages and spot-checking specific habitats or sites:

> https://discomap.eea.europa.eu/App/DiscodataViewer/?fqn=[EUNIS].[v1r8].[Habitat_Natura_2000]

### `eunis.habitats` R package
The most practical community solution for programmatic crosswalking between EUNIS versions and Annex I, maintained by Pattern Institute / CCMAR:

```r
install.packages("eunis.habitats")
library(eunis.habitats)


# Annex I → EUNIS Terrestrial 2021 (revised, but coastal not yet included)
crosswalk("1220", from = "Annex_I", to = "EUNIS_T_2021", unnest = TRUE)


# Browse the full EUNIS hierarchy
eunis_habitats |> dplyr::filter(startsWith(code, "B2"))
```

**Important:** The package uses bare Annex I codes (`1220`, not `H1220`). Strip any `H` prefix or `ANNEX1_` prefix before use. 


Documentation: https://www.pattern.institute/eunis.habitats/ · GitHub: https://github.com/patterninstitute/eunis.habitats

### EEA EUNIS Habitat Classification and Crosswalks (tabular)
Downloadable crosswalk tables: 

> https://www.eea.europa.eu/en/datahub/datahubitem-view/638330ea-90e6-4e41-81ea-e70f25ae7117

### EEA Reference Portal
Standard Data Form guidance and reference lists:

> https://cdr.eionet.europa.eu/help/natura2000

---

## Decisions Needed in the BMD Project

### Decision 1 — Annex I identifier format

- **A. Bare numeric** (`1220`) — matches EEA official format, Interpretation Manual, `eunis.habitats` package; best for joins and computation
- **B. `H`-prefixed** (`H1220`) — common in national databases and research tools; avoids ambiguity in mixed datasets; best for display and output
- **C. `ANNEX1_` prefixed** (`ANNEX1_1220`) — as used in EEA `habitat_unique_id` fields; verbose 


### Decision 2 — Which EUNIS version to use as the crosswalk target

??

### Decision 3 — How to handle the `eunis_components` list

The `[BISE].[latest].[Habitat_EUNIS_Classification]` table provides a hierarchical path per Annex I code. 
is this enough?
