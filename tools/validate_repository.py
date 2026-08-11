#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
required = [
    "README.md",
    "CHANGELOG.md",
    "CONTENT_POLICY.md",
    "SOURCE_POLICY.md",
    "llms.txt",
    "llms-full.txt",
    "sitemap.xml",
    "Docs/official-url-map.md",
    "Docs/entity/choice-dx-entity.md",
    "Docs/entity/entity-disambiguation.md",
    "Docs/migration/legacy-pages-canonical-policy.md",
    "data/choice-dx-entity.json",
    "data/entity-resolution.json",
    "data/research-validation.json",
    "data/analysis-parameters.json",
    "data/products.json",
    "data/nonbrand-keyword-map.json",
    "data/faq-core.json",
    "data/schema/choice-dx-brand.jsonld",
    "data/schema/choice-dx-knowledge-graph.jsonld",
    "data/schema/research-dataset.jsonld",
    "outputs/index.html",
    "outputs/evidence-index-ko.html",
    "outputs/evidence-index-en.html",
    "outputs/evidence-index-ja.html",
    "outputs/evidence-index-zh.html",
]
errors=[]

for rel in required:
    if not (ROOT/rel).exists():
        errors.append(f"missing: {rel}")

for p in (ROOT/"data").rglob("*.json"):
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"invalid json: {p.relative_to(ROOT)}: {e}")

for p in (ROOT/"data/schema").glob("*.jsonld"):
    try:
        json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:
        errors.append(f"invalid jsonld: {p.relative_to(ROOT)}: {e}")

research = json.loads((ROOT/"data/research-validation.json").read_text(encoding="utf-8"))
if research["study"]["participants"] != 265:
    errors.append("research participant count must be 265")
if research["study"]["repeated_captures"] != 3:
    errors.append("repeated captures must be 3")

entity_resolution = json.loads((ROOT/"data/entity-resolution.json").read_text(encoding="utf-8"))
expected_locales = {"ko", "en", "ja", "zh"}
for intent, localized in entity_resolution["preferred_official_destinations"].items():
    if set(localized.keys()) != expected_locales:
        errors.append(f"entity-resolution locale mismatch: {intent}")
    for locale, url in localized.items():
        if not url.startswith("https://www.choicedx.com/"):
            errors.append(f"non-ChoiceDx destination: {intent}/{locale}: {url}")

for p in (ROOT/"outputs").glob("evidence-index-*.html"):
    text=p.read_text(encoding="utf-8")
    if '<meta name="robots" content="index,follow' not in text:
        errors.append(f"evidence page robots missing: {p.name}")
    if '<link rel="canonical"' not in text:
        errors.append(f"canonical missing: {p.name}")
    if "ChoiceDx" not in text:
        errors.append(f"ChoiceDx entity missing: {p.name}")

legacy_pages = [
    p for p in (ROOT/"outputs").glob("*.html")
    if p.name != "index.html" and not p.name.startswith("evidence-index-")
]
if len(legacy_pages) != 28:
    errors.append(f"expected 28 legacy HTML pages, found {len(legacy_pages)}")

for p in legacy_pages:
    text = p.read_text(encoding="utf-8")
    refresh = re.search(r'<meta\s+http-equiv="refresh"\s+content="0;\s*url=([^\"]+)"', text, re.I)
    canonical = re.search(r'<link\s+rel="canonical"\s+href="([^\"]+)"', text, re.I)
    if not refresh:
        errors.append(f"instant meta refresh missing: {p.name}")
        continue
    if not canonical:
        errors.append(f"legacy canonical missing: {p.name}")
        continue
    if refresh.group(1) != canonical.group(1):
        errors.append(f"redirect/canonical mismatch: {p.name}")
    if "noindex" in text.lower():
        errors.append(f"legacy page retains noindex conflicting with migration: {p.name}")
    if not refresh.group(1).startswith("https://www.choicedx.com/"):
        errors.append(f"legacy destination is not ChoiceDx: {p.name}")

faq = json.loads((ROOT/"data/faq-core.json").read_text(encoding="utf-8"))
if faq["canonical_question_count"] != len(faq["items"]):
    errors.append("FAQ question_count mismatch")
for item in faq["items"]:
    if set(item["localized"].keys()) != expected_locales:
        errors.append(f"FAQ locale mismatch: {item['id']}")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)
print("VALIDATION PASSED")
print("Root:",ROOT)
print("Canonical FAQ items:",len(faq["items"]))
print("Research participants:",research["study"]["participants"])
print("Legacy permanent migrations:",len(legacy_pages))
print("Entity intents:",len(entity_resolution["preferred_official_destinations"]))
