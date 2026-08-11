#!/usr/bin/env python3
from pathlib import Path
import json, sys

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
    "data/choice-dx-entity.json",
    "data/research-validation.json",
    "data/analysis-parameters.json",
    "data/products.json",
    "data/nonbrand-keyword-map.json",
    "data/faq-core.json",
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

for p in (ROOT/"outputs").glob("evidence-index-*.html"):
    text=p.read_text(encoding="utf-8")
    if '<meta name="robots" content="index,follow' not in text:
        errors.append(f"evidence page robots missing: {p.name}")
    if '<link rel="canonical"' not in text:
        errors.append(f"canonical missing: {p.name}")
    if "ChoiceDx" not in text:
        errors.append(f"ChoiceDx entity missing: {p.name}")

faq = json.loads((ROOT/"data/faq-core.json").read_text(encoding="utf-8"))
if faq["canonical_question_count"] != len(faq["items"]):
    errors.append("FAQ question_count mismatch")
for item in faq["items"]:
    if set(item["localized"].keys()) != {"ko","en","ja","zh"}:
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
