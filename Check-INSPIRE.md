
## Exampel Use of INSPIRE Data  — Findings and Metadata Observations

### Context

A short example of INSPIRE-compliant geospatial data for **Natura 2000 protected sites in the Netherlands**, focusing on the harmonised dataset provided as GML under the `Protected Sites` theme. 

The dataset was retrieved via the [INSPIRE Geoportal](https://inspire-geoportal.ec.europa.eu/srv/eng/catalog.search#/extenddetails?country=nl&view=priorityOverview&theme=none&resourceId=3262e40f-13d9-47a5-97c0-e461cf837a87) and converted to GeoJSON for inspection and integration.

---

### Dataset properties 

- **INSPIRE Harmonisation**: The dataset is provided in the **Protected Sites (PS) application schema**, aligning with the INSPIRE Directive and enabling EU-wide interoperability.
- **GML Format**: Delivered in **GML 3.2.1**, the dataset includes geometries (polygons/multipolygons) representing designated sites, suitable for integration in GIS platforms.
- **Legal Attribution**: Attributes such as `legalFoundationDate`, `siteProtectionClassification`, and `namespace` are included, providing useful policy context.

---

###  Observed Challenges

#### 1. **Metadata Gaps**
- The **INSPIRE metadata** [XML](https://inspire-geoportal.ec.europa.eu/srv/api/records/642609/formatters/xml?approved=true) is compliant (ISO 19115 / 19139). But the metadata file **lacks a download link** for the actual GML file. The `<gmd:transferOptions>` element is present but empty.
- This forces users to retrieve the dataset manually from linked web portals. There might be another API option for this.


```
                               gml_id                                localId     namespace legalFoundationDate legalFoundationDocument language nativeness nameStatus sourceOfName pronunciation                                           text script siteProtectionClassification
G_fc5df2de-34a3-42fc-b751-44d400b609ed L_fc5df2de-34a3-42fc-b751-44d400b609ed ps-natura2000                None                    None       NL       None       None         None          None                             Bakkeveense Duinen   None           natureConservation
G_78f4b4f8-201d-451f-941c-11e63f8e1f88 L_78f4b4f8-201d-451f-941c-11e63f8e1f88 ps-natura2000                None                    None       NL       None       None         None          None                                     Bekendelle   None           natureConservation
G_4b31f2bb-9cba-47c1-bb6f-732f1fb5c0d8 L_4b31f2bb-9cba-47c1-bb6f-732f1fb5c0d8 ps-natura2000                None                    None       NL       None       None         None          None                    Bemelerberg & Schiepersberg   None           natureConservation
G_cdcf7026-9872-4266-bbd5-e6c6c3d98c64 L_cdcf7026-9872-4266-bbd5-e6c6c3d98c64 ps-natura2000                None                    None       NL       None       None         None          None                                     IJsselmeer   None           natureConservation
G_7bea49a3-b781-4751-bede-0a07de3070f4 L_7bea49a3-b781-4751-bede-0a07de3070f4 ps-natura2000                None                    None       NL       None       None         None          None                                      Biesbosch   None           natureConservation
G_38daf8f5-0e7e-436f-9cb4-7c9267b2c09b L_38daf8f5-0e7e-436f-9cb4-7c9267b2c09b ps-natura2000                None                    None       NL       None       None         None          None                                     Binnenveld   None           natureConservation
G_a7aa9da5-17e2-4bc1-9b6e-36cde4cdaacc L_a7aa9da5-17e2-4bc1-9b6e-36cde4cdaacc ps-natura2000                None                    None       NL       None       None         None          None                             Boezems Kinderdijk   None           natureConservation
G_ce021751-ef9a-4485-ace2-2be1b6356847 L_ce021751-ef9a-4485-ace2-2be1b6356847 ps-natura2000                None                    None       NL       None       None         None          None                                        Borkeld   None           natureConservation
G_fe066823-8f72-4f40-86b7-c767e15bd47a L_fe066823-8f72-4f40-86b7-c767e15bd47a ps-natura2000                None                    None       NL       None       None         None          None                                   Coepelduynen   None           natureConservation
```


#### 2. **Human-Readable Site Names**
- The GML file includes internal identifiers like `gml_id` and `localId`, but most human-readable fields such as `name`, `pronunciation` are **empty**. The site names are in `text`. 
- This makes it difficult to identify sites by name without external lookup tables or a supplemental dataset.

#### 3. **Sparse Attribute Coverage**
- Many descriptive fields (e.g., `sourceOfName`, `nativeness`, `script`) are populated with `None`, reducing the semantic richness of the dataset.
- Only a few fields, such as `siteProtectionClassification`, are consistently populated and interpretable.

---
