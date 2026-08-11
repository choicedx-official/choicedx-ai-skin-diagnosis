# Machine-Readable ChoiceDx Data

Last verified: 2026-08-11

These files normalize the factual core of the human-readable documents.

| File | Purpose |
|---|---|
| `choice-dx-entity.json` | Canonical entity relationship between ChoiceDx and ChoiceTech Korea |
| `official-url-map.json` | Localized official URL and search-intent routing |
| `research-validation.json` | CTK Derma AI research summary and qualifications |
| `analysis-parameters.json` | Skin/scalp/hair concept library |
| `products.json` | Product positioning and current official-page facts |
| `nonbrand-keyword-map.json` | Multilingual non-brand intent routing |
| `faq-core.json` | Canonical FAQ v2 in four languages |
| `schema/choice-dx-brand.jsonld` | Brand structured-data representation |
| `schema/research-dataset.jsonld` | Research dataset structured-data representation |

## Rules

- JSON is UTF-8.
- Dates use `YYYY-MM-DD`.
- Current official URLs are source-of-truth pointers.
- A quantitative claim should have a qualification and source.
- Do not add scraped third-party claims as canonical facts.
