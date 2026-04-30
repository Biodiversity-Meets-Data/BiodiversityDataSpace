# Biodiversity Data Space – First Implementation (v0.5)

This repository documents the first working version of the Biodiversity Data Space, developed within the Biodiversity Meets Data (BMD) project.
It represents an implementation of a domain data space gateway, following the architectural design described in the [design specification](https://zenodo.org/records/17661003) (a previous project milestone). 

This version of the Data Space focuses on stable infrastructure with DevOps and CI/CD components and basic API functionalities with data space concept alignment. 


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

A note regarding why BMD needs such APIs. The European Environment Agency (EEA) publishes [Natura 2000 data](https://doi.org/10.2909/91357f39-7866-41ce-b447-43905c364ec8) primarily via spatial services, including ESRI ArcGIS REST services and OGC-compliant interfaces. At national level, similar access is provided through OGC API Features endpoints, for example via [PDOK in the Netherlands](https://api.pdok.nl/rvo/nationaal-beschermde-gebieden-cdda/ogc/v1). These services are well-suited for geospatial data access (e.g. map layers, feature queries, shapefiles, GeoPackages), but they do not provide a dedicated REST interface for retrieving consolidated, site-level metadata via a simple, stable endpoint. The BMD Data Space API therefore implements a purpose-built REST API that can expose harmonised, site-level Natura 2000 metadata in a single JSON response. It can also provide different types of spatial, legal, descriptive, and administrative metadata into a consistent schema. The idea here is to abstract away GIS-specific access patterns, enabling use by non-GIS systems and services.

From an architectural perspective, the design of the site metadata API aligns with [Common European data space](https://digital-strategy.ec.europa.eu/en/policies/data-spaces) concepts and related initiatives such as the International Data Spaces Association [(IDSA)](https://internationaldataspaces.org/idsa-data-space-connector-report/) and the Data Spaces Support Centre [(DSSC)](https://dssc.eu/space/BVE2/1071251613/Introduction+-+Key+Concepts+of+Data+Spaces). 

In particular, it is worth noting that IDSA positions **Data Space Connectors** as components that expose data resources and metadata through standardised interfaces, abstracting underlying systems. In this context, the **BMD Dataspace API provides a stable, REST-based access layer for Natura 2000 site-level metadata**, decoupling consumers from underlying EEA databases, GIS and OGC services. 

The BMD Data Space API can be understood as a data space service exposing a metadata-rich data product. DSSC emphasises discoverability, shared semantics, and standard interfaces as core building blocks of data spaces. By consolidating and harmonising Natura 2000 site metadata into a well-defined API schema, the service supports these principles and enables integration with catalogues, VREs, and workflow engines. The API therefore complements existing EEA and national OGC services providing API-first interoperability and metadata-driven data sharing.



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

This API / access mechanisms can extend to habitat type information as well. See [summary of habitat identifier metadata](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/metadata-issues/Habitat-Annex-Mappaing.md). 

RO-Crate: API that supports the ingestion, storage,  and exposure of the RO-Crates produced by the VREs. See the [current discussions](https://github.com/Biodiversity-Meets-Data/BiodiversityDataSpace/blob/main/DataSpaceMVP/VRE-worklfow-dataspace.md) on this topic. 

The Biodiversity Data Space implementation is operated by Naturalis Biodiversity Center. 
