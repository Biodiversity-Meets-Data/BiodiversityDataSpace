check [this blog post](https://www.linkedin.com/posts/sharif-islam-92999227_productive-sunday-afternoon-ideas-are-brewing-activity-7395823230047010816-VB7P?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAWph7EBFHXu_634mWX092rS-pv7Rp1xUCo) for more details and background: 

| Database/System           | Identifier | Purpose                           |
|---------------------------|-----------|-----------------------------------|
| Sovon (Dutch monitoring)  | 2310      | National bird monitoring          |
| Observation.org           | 349       | Citizen science platform          |
| GBIF                      | 2480420   | Global biodiversity occurrences   |
| EUNIS (EEA)               | 1195      | European conservation status      |
| Natura2000                | A072      | Legal protection framework        |
| NCBI Taxonomy             | 43551     | Genomic sequence data             |
| Wikidata                  | Q170466   | Linked open data                  |
| Catalogue of Life         | 4F6YZ     | Taxonomic authority / checklist  |


What if we treat species identifiers in the biodiversity data landscape the same way commercial organisations treat customers? Hear me out...

We have seen this problem in biodiversity data. Species names and related identifiers appear differently across databases. Reports use one identifier, PDFs reference another, static datasets export yet another. We try to link them matching scientific names, fuzzy string matching, hoping they all align. This isn't new.

```

European Honey Buzzard (Pernis apivorus)
│
├─ Policy & Conservation Frameworks
│  ├─ EU Birds Directive: A072
│  ├─ EUNIS: 1195
│  └─ Natura 2000: A072
│
├─ National Monitoring Systems / Citizen science  
│  ├─ Sovon (Netherlands): 2310
│  ├─ Observation.org: 349
│  └─ [Other national databases...]
│
├─ Global Biodiversity Platforms / Checklist 
│  ├─ GBIF: 2480420
│  └─ Wikidata: Q170466
|  └─ Catalogue of Life: 4F6YZ 
│
├─ Genomics & Taxonomy
│  ├─ NCBI Taxonomy: 43551
│
└─ Synonyms & Historical Names
   └─ Falco apivorus Linnaeus, 1758

```
