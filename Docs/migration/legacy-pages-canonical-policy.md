# Legacy GitHub Pages Migration Policy

Last updated: 2026-09-21

## Phase 1: Research and combined product guide

This section supersedes the historical v3 redirect rule **only for these existing
filename families**, in `ko`, `en`, `ja`, and `zh` (12 HTML pages):

- `outputs/guidebook-why-accurate-skin-diagnosis-*.html`
- `outputs/guidebook-accurate-skin-diagnosis-customer-trust-*.html`
- `outputs/guidebook-skin-analyzer-device-vs-software-*.html`

Keep every URL accessible with HTTP 200, remove the existing instant meta refresh,
and use `<meta name="robots" content="noindex, follow">` in `<head>`. Retain exactly
one verified, same-language official canonical and show a localized link at the
start of the body. Do not add JavaScript redirects or block crawling in robots.txt.

The two Research families map to `/research`, `/en/research`, `/ja/research`, and
`/zh/research` on `https://www.choicedx.com`. The combined product guide maps to the
corresponding `/product` hub, which includes both Dx-Smart and Dx-Pico, and includes
direct links to the official pages for both products. Do not create standalone
Dx-Smart or Dx-Pico GitHub Pages or select one product as the canonical for a
combined product page. All eight canonical destinations were checked on
2026-09-21: HTTP 200, correct page language, and matching official self-canonical.

These 12 URLs were already absent from the existing five-entry sitemap. Keep them
excluded. The repository robots.txt remains unchanged. The origin-root robots.txt
returned 404 on 2026-09-21; the project-subdirectory robots.txt is not the origin's
crawler policy. Do not introduce a root-level Disallow rule.

The other 16 historical redirect pages and five evidence-navigation HTML files
remain unchanged during this first rollout. Preserve README, Markdown, JSON,
JSON-LD and assets. The audit also found 48 additional HTML pages generated from
Markdown, including four Research summaries and four product guides; record these
separately for a later decision instead of silently expanding this rollout.

The goal of `noindex` is removal from search results after recrawling. A canonical
is a preference signal; this combination does not guarantee ranking-signal transfer
or immediate replacement in search results. Google advises against using noindex
solely to choose a canonical within a site; this phase explicitly prioritizes
removing the legacy URLs from indexing as requested.

Sources:
- https://developers.google.com/search/docs/crawling-indexing/block-indexing
- https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls

## Goal

Historical `outputs/` pages were published before the current ChoiceDx.com information architecture was finalized. Some of those pages accumulated crawl history or backlinks, but they now overlap with stronger official ChoiceDx pages. The migration policy therefore preserves URL continuity while consolidating indexing signals toward the current ChoiceDx-owned destination.

## Historical v3 migration rule (remaining pages only)

### New evidence-index pages
The current `outputs/evidence-index-*.html` pages:
- contain GitHub-specific evidence navigation rather than duplicate commercial copy;
- may remain indexable when they provide unique structured navigation;
- should self-canonicalize to their GitHub Pages URL;
- should link clearly to the relevant ChoiceDx.com source-of-truth pages.

### Legacy marketing / guidebook pages
When a historical GitHub Page has a clear current ChoiceDx replacement:

1. preserve the historical URL for backlink and bookmark continuity;
2. replace the duplicate long-form article with a minimal migration page;
3. use an **instant 0-second `meta refresh`** to the closest existing localized ChoiceDx page;
4. set `rel="canonical"` to the same destination as the redirect;
5. keep a visible fallback link for accessibility and browsers that do not follow meta refresh;
6. do not point different signals to different destinations;
7. do not redirect to a generic homepage when a more specific live replacement exists.

Google Search documents instant `meta refresh` as a permanent redirect signal when server-side redirects cannot be implemented. GitHub Pages does not provide repository-level HTTP 301 configuration for these static legacy files, so instant meta refresh is used as the practical migration mechanism.

## Recommended mapping

| Legacy theme | Preferred ChoiceDx destination |
|---|---|
| Skin Scan explainer | localized References / case-study hub |
| Accurate analysis / customer trust | localized Research |
| Data-driven retail consultation | localized References |
| Integrated skin/scalp/hair analysis | localized AI Analysis Solution |
| Analyzer device vs software | localized Product hub |
| Why accurate skin analysis matters | localized Research |
| Olive Young Skin Scan result guide | localized References |

## Language rule

A legacy page should redirect to a canonical destination in the **same language whenever that localized destination exists**.

- Korean → Korean ChoiceDx URL
- English → `/en/`
- Japanese → `/ja/`
- Simplified Chinese → `/zh/`

## Historical v3 cautions (remaining redirect pages only)

- Do not keep duplicate full articles indexable on GitHub Pages and ChoiceDx.com.
- Do not combine `noindex` with a migration redirect when the intent is to consolidate a moved URL; use one clear permanent-migration signal.
- Do not canonicalize every page to the homepage.
- Do not point the canonical and redirect to different URLs.
- Do not redirect to a URL that returns 404 or to a wrong-language page.
- Do not recreate new long-form SEO landing pages on GitHub that compete with ChoiceDx.com.
