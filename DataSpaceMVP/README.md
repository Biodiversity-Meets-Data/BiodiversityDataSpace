# Biodiversity Data Space – First Implementation (v0.5)

This repository documents the first working version of the Biodiversity Data Space, developed within the Biodiversity Meets Data (BMD) project.
It represents an implementation of a domain data space gateway, following the architectural design described in the design specification. See [Zenodo record](https://zenodo.org/records/17661003).

This version focuses on stable infrastructure with DevOps and CI/CD components and basic API functionalities with data space concept alignment. 


## What this version provides

API-based access to data products, with a focus on:

- Natura 2000 site metadata

- Geospatial representations (GeoJSON)

Data space–aligned metadata, including:

- Dataset provenance (DCAT / PROV)

- Licensing and attribution

- Clear roles of data providers and service operators

A domain-level data space identity, aligned with:

- the European Green Deal Data Space

- EOSC principles

## API examples (illustrative)

Endpoints are evolving, but current examples include: 

DataSpace description: 


/version 
```
{
  "dataSpace": {
    "id": "urn:dataspace:biodiversity",
    "name": "Biodiversity Data Space",
    "domain": "biodiversity",
    "description": "The Biodiversity Meets Data (BMD) project is creating a data space using cloud-native open infrastructure to support biodiversity monitoring, conservation, and policy across terrestrial, freshwater, and marine environments.",
    "governanceRole": "DomainDataSpace",
    "alignment": [
      "European Green Deal Data Space",
      "EOSC"
    ]
  },
  "projectContext": {
    "projectName": "Biodiversity Meets Data",
    "fundingProgramme": "Horizon Europe",
    "cordis": "https://doi.org/10.3030/101181294",
    "roleInDataSpace": "Initial implementation and pilot use cases"
  },
  "version": {
    "api": "0.0.6",
    "commit": "d29b3c9",
    "branch": "develop",
    "buildDate": "2026-01-22 08:22:46 UTC"
  },
  "service": {
    "name": "Biodiversity Data Space API",
    "type": "DataSpaceGateway",
    "capabilities": [
      "data-product-discovery",
      "metadata-exchange",
      "provenance-tracking"
    ]
  },
  "implementation": {
    "operator": "Naturalis Biodiversity Center"
  }
}
```



Natura 2000 site metadata
/sites/{siteId}/metadata
(e.g. site-level metadata, provenance, license, attribution)

GeoJSON representations for spatial integration
/sites/{siteId}
```
{
  "areaHa": 12.1,
  "areaKm2": null,
  "countryCode": "AT",
  "countryName": null,
  "dateCompilation": "1995-05-01T00:00:00Z",
  "dateConfSci": null,
  "datePropSci": "1998-05-01T00:00:00Z",
  "dateSac": "2008-06-01T00:00:00Z",
  "dateSpa": null,
  "dateUpdate": null,
  "designation": "AT03...100%",
  "documentation": "Koo, A.J., 1994  Pflegekonzept f. d. Naturschutzgebiete d. Burgenlandes. BFB Biol. Forsch. Bgld. Bericht 82, pp203",
  "explanations": null,
  "inspireId": null,
  "latitude": 47.9556,
  "lengthKm": 0,
  "longitude": 17.0508,
  "marineAreaPercentage": 0,
  "othercharact": "Am Ostrand der Parndorfer Platte eine Geländekante, die steil zur Leithaniederung abfällt. Quarzreiche pannone Sande und Schotter führten zur Entstehung stark saurer Böden. Die Grobkörnigkeit der Sedimente, sowie die austrocknende Wirkung des Windes, verbunden mit einer nur schwach ausgebildeten Humusschicht im Hangbereich führten zur Ausbildung einer artenreichen Trockenrasen Gesellschaft. Im Bereich des Hangfußes schließen Mähwiesen an.",
  "quality": "Der Artenreichtum des Silikattrockenrasens macht diesen Standort zu einem wichtigen Element der pannonischen Lebensräume. In Folge der Flachgründigkeit und der  Steilheit der Trockenrasen sind diese trotz über Jahre fehlender Beweidung in einem repräsentativen Zustand erhalten geblieben.",
  "sacLegalReference": "Verordnung der Burgenländischen Landesregierung vom 3. Juni 2008 über die Erklärung des Naturschutzgebietes Nickelsdorfer Haidel zum Europaschutzgebiet (\"Europaschutzgebiet Nickelsdorfer Haidel\"). Landesgesetzblatt Nr. 56/2008",
  "siteCode": "AT1101112",
  "siteName": "Nickelsdorfer Haidel",
  "siteType": "B",
  "spaLegalReference": null
}
```
provenance: 
```
{
  "@type": "dcat:Dataset",
  "@id": "AT1101112",
  "dct:title": "Natura 2000 Site AT1101112 – Nickelsdorfer Haidel",
  "dct:publisher": {
    "name": "European Environment Agency",
    "identifier": "urn:participant:eea"
  },
  "dct:source": "https://www.eea.europa.eu/data-and-maps/data/natura-2000 ",
  "dct:license": {
    "id": "CC-BY-4.0",
    "name": "Creative Commons Attribution 4.0"
  },
  "prov:wasDerivedFrom": [
    "EEA Natura 2000 Dataset"
  ],
  "prov:wasAttributedTo": [
    "European Environment Agency",
    "Naturalis Biodiversity Center"
  ],
  "dataspace:role": {
    "EEA": "DataProvider",
    "Naturalis": "ServiceProvider"
  }
}
```

RO-Crate: 



The implementation is operated by Naturalis Biodiversity Center. 

