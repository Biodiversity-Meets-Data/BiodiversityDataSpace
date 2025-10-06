# Natura 2000 FAIR Data 

## Challenge 
The information attached to each Natura 2000 site represents imporant metadata for our Biodiversity Data Space. 
However, this information is often scattered across different files and API endpoints, 
lacking standardisation and ontology mapping. This is an initial effort to provide a solution that needs adoption within the BMD project.

Here's a snippet of data about a site in Austria, obtained from the [EEA Data Explorer](https://discodata.eea.europa.eu/index.html#) where you can make SQL queries against the database:

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
 There are files like `Natura2000_end2021_rev1_dataset_definition_SPECIES.csv` from [EEA SDI](https://sdi.eea.europa.eu/data/5a2409fc-6ded-45d4-a161-5278c3c2e3a7).
 These data definitions have critical field definitions and code lists. For instance, from this csv we can find out that "p" means *permanent* and population_type means *Population status for the species*


>cat Natura2000_end2021_rev1_dataset_definition_SPECIES.csv
Element name,Element definition,Value definitions
COUNTRY_CODE,Two digit country code the site belongs to.,
SITECODE,Unique code witch forms the key-item within the database.,"The unique code comprises nine characters and consists of two components. The first two codes are the country code the remaining seven characters, which serve to create a unique alphanumeric code for each site."
SPECIESNAME,Scientific name of the protected species.,
SPECIESCODE,Code the species listed in Article 4(1) and 4(2) of the bird directive 79/409/EEC and Annex II of Council Directive 92/43/EEC.,
REF_SPGROUP,Species Group from the reference ETC lookup species list.,"Reptiles, Birds, Amphibians, Mammals, Invertebrates, Fish, Plants"
SPGROUP,Species Group.,"Reptiles, Birds, Amphibians, Mammals, Invertebrates, Fish, Plants"
SENSITIVE,States if a species is sensitive or not for its publication.,0: no sensitive; 1: sensitive
NONPRESENCEINSITE,In case that a species no longer exists in the site a value "1" is entered.,
POPULATION_TYPE,Population status for the species.,p: permanent; r: reproducing; c: concentration; w: wintering
LOWERBOUND,Lower limits for the species population size.,
UPPERBOUND,Upper limits for the species population size.,
COUNTING_UNIT,"Units of population, i = individuals, p = pairs or other units according to the standard list of population units and codes in accordance with Article 12 and 17 reporting.",
ABUNDANCE_CATEGORY,Species population abundance category.,C: common; R: rare; V: very rare; P: present
DATAQUALITY,Assessment of the quality of data provided for habitats.,G: 'Good' (e.g. based on surveys); M: 'Moderate' (e.g. based on partial data with some extrapolation); P: 'Poor' (e.g. rough estimation)
POPULATION,Size and density of the population of the species present on the site in relation to the populations present within national territory.,A: 100% >= p > 15%; B: 15% >=p> 2%; C: 2% >=p> 0%; D: non-significant population
CONSERVATION,Degree of conservation of the features of the habitat important for the species.,A: conservation excellent; B: good conservation; C: Average or reduced conservation
ISOLATION,Degree of isolation of the population present on the site in relation to the natural range of the species.,"A: population (almost) isolated; B: population not-isolated, but on margins of area of distribution; C: population not-isolated within extended distribution range."
GLOBAL,Global assessment if the value of the site for conservation of the species concerned.,A: excellent value; B: good value; C: significant value.
INTRODUCTION_CANDIDATE,Species referred to in Article 4 of Directive 2009/147/EC or species listed in Annex II to Directive 92/43/EEC considered as a candidate for introduction on the site.,

The data and its documentation live in separate places which is ok but they are not linked in a machine readable manner. **Metadata as description of the data should be attached to the data but also stored somewhere else**. 


There are also INSPIRE specific xml and gml files which is found in the EEA site but also in national portals like https://api.pdok.nl/rvo/natura2000-geharmoniseerd/ogc/v1/collections/protectedsite

To make this data FAIR, we can do a few things. Use established ontologies: 

- **Schema.org** for general structure and properties 
- **Darwin Core** for species and measurements  
- **DCAT** for dataset metadata
- **EIOnet vocabularies** for environmental concepts
- **QUDT** for measurements and units

## Example Transformation

```json
{
  "@context": {
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

INSPIRE defines (https://github.com/INSPIRE-MIF/technical-guidelines/blob/main/data/ps/dataspecification_ps.adoc) the structure and core attributes of Protected Sites (geometry, site code, name, designation, legal references). 
Our JSON-LD serialisation needs to incorporates these as well. 

A simple JSON example demonstrating FAIR is here [here](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/bmd-site-example.json).
A more elaborate JSON-LD example: is [here](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/AT1101112_FAIR.jsonld)

We can use this example to create a template (similar to RO-Crate template) for site description and attached datasets or attached species/habitats. There will be also a need to map the species ids. For instance, 
AT1101112 site has species eunis_id 154421 (https://eunis.eea.europa.eu/species/154421). This maps to GBIF https://www.gbif.org/species/3121387 but hidden in another table. 
```
{
        "code_site": "AT1101112",
        "id_eunis": 154421,
        "code_2000": "1917",
        "species_name": "Artemisia pancicii",
        "species_group_name": "Flowering Plants",
        "picture_url": ""
    },
```

JSON-LD / RO-Crate templates could make this a bit more structure and FAIR. 
