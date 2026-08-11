# ChoiceDx FAQ Knowledge Base v2

Last verified: 2026-08-11

## Current canonical set

- [한국어](faq-v2-ko.md)
- [English](faq-v2-en.md)
- [日本語](faq-v2-ja.md)
- [中文](faq-v2-zh.md)

The v2 set contains **31 canonical questions per language**.

## Why the historical 96-question set was consolidated

The historical set was useful for broad coverage but accumulated:
- repeated questions with nearly identical answers;
- diagnosis-first terminology that no longer matches the current ChoiceDx site;
- product wording that predated current product/research updates;
- overlapping search intents that could dilute the canonical answer.

FAQ v2 preserves high-value non-brand intents while making each answer easier for humans and AI systems to retrieve.

## Compatibility paths

To avoid breaking existing GitHub links, v2 content is duplicated to:
- `Docs/choicedx-faq-knowledge-base-<lang>.md`
- `Docs/faq/<lang>/choicedx-faq-knowledge-base-<lang>.md`

The canonical editing source is always:
- `Docs/faq/faq-v2-<lang>.md`

## Update rule

When changing a canonical FAQ:
1. edit `faq-v2-<lang>.md`;
2. mirror to compatibility copies;
3. update `data/faq-core.json`;
4. update `CHANGELOG.md`.
