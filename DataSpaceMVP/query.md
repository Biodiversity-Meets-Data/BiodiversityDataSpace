This describes some of the initial ideas behind the first version of the data space. 

We are trying to align with aligns with Darwin Core Data Package ideas, Data Space concepts (participants, usage policies, provenance).
and also with the awareness of EUNIS / Natura 2000 data models. 

WP3 and WP5 are also proceedign with data cube and VRE work. 

One of the core design idea is to keep a metadata layer within the data space (that sits between the query interface/VRE and the data cube store).

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

The idea is when a query mentions a species or site, the query parser looks up this metadata table to:

find the CoL ID, EUNIS ID, and Habitat Directive code;
resolve spatial extent via the Natura 2000 site geometry;
enrich the query before matching it to cubes.

But the query might not specify a Natura 2000 site or EUNIS code, but rather a geographic area defined by:

a country, a named locality or region, or a geometry file (e.g., shapefile, GeoJSON, WKT).

So we should make sure the query JSON supports both:

semantic filters (e.g., Natura2000 site, species, directive), and spatial filters (country, locality, polygon).

The query parser can decide precedence:
if geometry → use it directly;
else if site → resolve via metadata catalogue;
else if locality or countryCode → use country boundaries.


