# ChoiceDx Knowledge Hub Changelog

## 2026-09-21 — Phase 2 Markdown document cleanup

- Add `noindex, follow` only to the four Research and four product guide documents.
  Research uses language-matched official canonicals and visible source links;
  product guides retain their generated GitHub Pages self-canonicals.
- Override Primer 0.6.0's default layout with `page.lang`, then `site.lang`, then
  `en-US`. Add matching `lang` metadata to all 32 localized Markdown sources.
- Refresh verified hardware counts in product guides, FAQ v2, product JSON and
  `llms-full.txt`: Smart 10/9, Prime 10/9, Pico 10/10, Self 9/8 (English source).
- Match the official Skin 2 release threshold: English and structured summaries
  say at least 20% (>=20%), not more than 20% (>20%), versus the prior company system.
- Preserve the software-specific eight-parameter Pro Skin description. Attribute
  Smart magnification to the Korean source and flag differing Japanese/Chinese
  official values without inventing a universal replacement specification.
- Add source and rendered-page checks using the GitHub Pages Jekyll runtime.
- Preserve all 33 existing static HTML files, robots.txt, sitemap.xml, the phase 1
  migration policy and the indexing policy of the other 40 Markdown documents.
- Save the pre-change commit `da76549712b9f363f36839d724a32ecb8b3d6bf7` on
  `backup-before-phase2-2026-09-21`.

## 2026-09-21 — Phase 1 legacy search cleanup

- Keep 12 existing Research and combined product guide URLs; replace instant meta
  refresh with `noindex, follow`, verified localized official canonicals and visible links.
- Keep `/product` as the combined guide destination and add direct official Dx-Smart
  and Dx-Pico links. Do not create independent product pages.
- Strengthen the README's official website and Research links; document the phased policy.
- Preserve robots.txt, the sitemap (these URLs were already absent), all other HTML,
  reference Markdown, structured data and assets. The official website is unchanged.
- Save the pre-change commit `2d00810cff741c66300bedaa78c322431749d858` on
  `backup-before-seo-cleanup-2026-09-21` before editing.

## 2026-08-11 — v2.1 SEO/GEO Hardening

### Entity & GEO
- Added `data/entity-resolution.json` to distinguish ChoiceTech Korea corporate/manufacturer intent from ChoiceDx AI analysis intent.
- Added `Docs/entity/entity-disambiguation.md` for human-readable entity resolution.
- Added connected JSON-LD knowledge graph linking ChoiceTech Korea → ChoiceDx → website → official hubs → Dx-Smart / Dx-Prime / Dx-Pico / Dx-Self.
- Expanded `llms.txt` with preferred multilingual non-brand destinations and canonical entity rules.

### Legacy URL migration
- Upgraded 28 historical GitHub Pages from `noindex,follow + canonical` notices to **instant 0-second meta-refresh migrations** plus matching canonical URLs.
- Kept each migration destination language-matched: KO → KO, EN → EN, JA → JA, ZH → ZH.
- Preserved visible fallback links for accessibility and browser compatibility.
- Updated migration policy to prevent conflicting `noindex`, redirect and canonical signals.

### Retrieval quality
- Updated the machine-readable data index to include entity-resolution and connected knowledge-graph files.
- Reinforced the rule that broad AI skin/scalp/hair analysis intent belongs to ChoiceDx, while company/manufacturer intent belongs to ChoiceTech Korea.

## 2026-08-11 — v2.0 Renewal

### Architecture
- Repositioned GitHub from a duplicate marketing/evidence blog into a **structured evidence and machine-readable knowledge layer**.
- Kept ChoiceDx.com as the primary owned-content and commercial domain.
- Added explicit ChoiceTech Korea ↔ ChoiceDx entity separation.

### Terminology
- Changed canonical terminology from **Diagnosis** to **Analysis** across entity definitions, navigation and structured data.
- Retained diagnosis/diagnostic-device equivalents only as secondary search synonyms.

### Multilingual SEO/GEO
- Added Korean, English, Japanese and Simplified Chinese non-brand keyword routing maps.
- Added preferred official URL mapping for AI skin analysis, analysis parameters, skin analyzers, scalp analyzers, validation, self-service kiosks and use cases.

### Research
- Added 4-language Research & Validation documents.
- Structured current study facts: 265 participants, Fitzpatrick I–VI, 3× repeated captures, standardized capture, Capture Calibration, AI quantitative analysis and expert-assessment comparison.
- Added explicit study-scope qualifications to avoid universal accuracy claims.

### Products & Measurement
- Added 4-language product guides and analysis-parameter guides.
- Added current product positioning for Dx-Smart, Dx-Prime, Dx-Pico, Dx-Self, ChoiceDx Pro Skin/Hair, DxPro Skin 2 and DxPro Hair 2.

### FAQ
- Replaced the historical 96-question baseline with **Canonical FAQ v2: 31 normalized questions per language**.
- Preserved old FAQ paths as compatibility/deprecation pointers.

### Pages & Crawling
- Added unique GitHub evidence-index pages rather than new duplicate commercial articles.
- Added focused sitemap, robots and AI-discovery files.
- Established explicit migration mappings from legacy GitHub Pages to current ChoiceDx official pages.
