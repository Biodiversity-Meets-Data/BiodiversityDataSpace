# Natura 2000 FAIR Data 

The information attached to each Natura 2000 site represents imporant metadata for our Biodiversity Data Space. 
However, this information is often scattered across different files and API endpoints, 
lacking standardisation and ontology mapping. This is an initial effort to provide a solution that needs adoption within the BMD project.

Here's a snippet of data about a site in Austria, obtained from the EEA Data Explorer where you can make SQL queries against the database:

```sql
SELECT * FROM [BISE].[latest].[Site_Species_List_Details] where site_code='AT1101112'
```

**Sample Data:**
```json
{
  "site_code": "AT1101112",
  "species_name": "Artemisia pancicii",
  "species_code": "1917",
  "id_eunis": 154421,
  "species_group_name": "Flowering Plants",
  "scientific_name": "Artemisia pancicii",
  "code_2000": "1917",
  "lower_bound": 20,
  "upper_bound": 100,
  "counting_unit": "i",
  "population_type": "p",
  "appears_number_sites": 7,
  "E27_threat_code": "VU",
  "E27_threat_name": "Vulnerable",
  "EU_threat_code": "DD",
  "EU_threat_name": "Data Deficient",
  "WO_threat_code": "DD",
  "WO_threat_name": "Data Deficient",
  "site_name": "Nickelsdorfer Haidel",
  "habitat_unique_id": "ANNEX1_6510"
}
```

**From a machine readability perspective, this is problematic**. For instance there is no description of what `"population_type": "p"` is supposed to mean.


Our source data exists in two separate components:

### 1. SQL API Endpoint
- **Source**: `SELECT * FROM [BISE].[latest].[Site_Species_List_Details] where site_code='AT1101112'`


### 2. CSV Data Definitions  
 Files like `Natura2000_end2021_rev1_dataset_definition_SPECIES.csv` from [EEA SDI](https://sdi.eea.europa.eu/data/5a2409fc-6ded-45d4-a161-5278c3c2e3a7)
 This has critical field definitions and code lists
 Values like `p: permanent; r: reproducing` for `POPULATION_TYPE`

The data and its documentation live in separate silos. 

There are also INSPIRE specific xml and gml files. 


To make this data FAIR, we can do a few things. ap it to established ontologies:

- **Schema.org** for general structure and properties 
- **Darwin Core** for species and measurements  
- **DCAT** for dataset metadata
- **EIOnet vocabularies** for environmental concepts
- **QUDT** for measurements and units

## Example Transformation

```json
{
  "@context": {
    // Integrated definitions from CSV files
    "population_type": "natura:populationType",
    "p": "natura:populationType/Permanent",
    "i": "http://qudt.org/vocab/unit/Individual"
  },
  "@type": "dcat:Dataset",
  "about": {
    "@type": "ProtectedSite",
    "siteCode": "AT1101112",
    "name": "Nickelsdorfer Haidel",
    "containsPlace": [
      {
        "@type": "natura:AnnexIHabitat",
        "habitatID": "ANNEX1_6240",
        "supports": {
          "@type": "dwc:Organism",
          "taxon": {
            "@type": "dwc:Taxon",
            "scientificName": "Artemisia pancicii"
          },
          "natura:populationEstimate": {
            "qudt:lowerBound": 20,
            "qudt:upperBound": 100,
            "qudt:unit": "http://qudt.org/vocab/unit/Individual"
          }
        }
      }
    ]
  }
}
```

INSPIRE defines the structure and core attributes of Protected Sites (geometry, site code, name, designation, legal references). 
Our JSON-LD serialisation needs to incorporates these as well. 

A simple JSON example demonstrating FAIR compliance is available here.

## Benefits

- **Self-describing data**: No external documentation needed
- **Machine actionable**: Enables sophisticated ecological queries
- **Interoperable**: Compatible with global biodiversity data portals
- **FAIR compliant**: Findable, Accessible, Interoperable, Reusable
