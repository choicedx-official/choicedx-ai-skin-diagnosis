# Legacy GitHub Pages Migration Policy

Last verified: 2026-08-11

## Goal

Historical `outputs/` pages were published before the current ChoiceDx.com information architecture was finalized. Some of those pages accumulated crawl history or backlinks, but they now overlap with stronger official ChoiceDx pages. The migration policy therefore preserves URL continuity while consolidating indexing signals toward the current ChoiceDx-owned destination.

## v3 migration rule

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

## What not to do

- Do not keep duplicate full articles indexable on GitHub Pages and ChoiceDx.com.
- Do not combine `noindex` with a migration redirect when the intent is to consolidate a moved URL; use one clear permanent-migration signal.
- Do not canonicalize every page to the homepage.
- Do not point the canonical and redirect to different URLs.
- Do not redirect to a URL that returns 404 or to a wrong-language page.
- Do not recreate new long-form SEO landing pages on GitHub that compete with ChoiceDx.com.
