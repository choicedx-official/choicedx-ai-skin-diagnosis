# ChoiceDx Documentation Index

Last verified: 2026-08-11

This directory contains the human-readable source layer for ChoiceDx structured evidence and entity disambiguation.

## Directory map

```text
Docs/
├─ entity/
│  ├─ choice-dx-entity.md
│  ├─ entity-disambiguation.md
│  └─ terminology-policy.md
├─ research/
│  └─ research-validation-{ko,en,ja,zh}.md
├─ measurement/
│  └─ analysis-parameters-{ko,en,ja,zh}.md
├─ products/
│  └─ product-guide-{ko,en,ja,zh}.md
├─ use-cases/
│  └─ use-cases-{ko,en,ja,zh}.md
├─ keywords/
│  └─ nonbrand-keywords-{ko,en,ja,zh}.md
├─ faq/
│  └─ faq-v2-{ko,en,ja,zh}.md
├─ migration/
│  ├─ deprecated-terms.md
│  └─ legacy-pages-canonical-policy.md
└─ official-url-map.md
```

## Editorial principle

The official ChoiceDx website is the primary source for current commercial content. These documents normalize facts, entity relationships, search terminology and source routing for verification, retrieval and AI-readable use.

## Entity rule

- ChoiceTech Korea = company / developer / manufacturer / operator.
- ChoiceDx = AI skin, scalp and hair analysis solution brand.
- Non-brand analysis and analyzer intent should route to ChoiceDx official pages.
- Corporate/manufacturer intent should route to ChoiceTech Korea.

See `entity/entity-disambiguation.md` for the full rule set.

## Legacy FAQ compatibility

The root-level `choicedx-faq-knowledge-base-*.md` files are retained only as compatibility pointers. Current FAQ knowledge is maintained in `Docs/faq/faq-v2-*.md`.
