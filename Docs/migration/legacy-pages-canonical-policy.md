# Legacy GitHub Pages Canonical & Indexing Policy

Last verified: 2026-08-11

## Problem being corrected

The historical `outputs/` library contains long-form pages created before the current ChoiceDx website structure was finalized. Some legacy pages self-canonicalize to GitHub Pages, while other pages point to old or inconsistent canonical destinations. That mixed policy makes it unclear whether GitHub or ChoiceDx.com should be treated as the primary source.

## v2 rule

### New evidence-index pages
The new `outputs/evidence-index-*.html` pages:
- contain structured, GitHub-specific evidence navigation;
- do not duplicate a ChoiceDx commercial landing page;
- may remain `index,follow`;
- self-canonicalize to their GitHub Pages URL.

### Legacy marketing/guidebook pages
When a legacy page substantially overlaps a current ChoiceDx-owned page:
1. preserve the URL for backlink continuity;
2. replace the content with a concise migration notice;
3. use `<meta name="robots" content="noindex,follow">`;
4. set canonical to the closest **existing** ChoiceDx official page;
5. provide a visible link to that official page;
6. do **not** use a fake or non-existent canonical URL.

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

## What not to do

- Do not delete all legacy URLs at once if they have backlinks.
- Do not canonicalize every page to the homepage.
- Do not set a canonical to a URL that returns 404.
- Do not keep duplicated full articles indexable on both GitHub Pages and ChoiceDx.com.
