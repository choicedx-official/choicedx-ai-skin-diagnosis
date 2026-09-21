#!/usr/bin/env python3
from pathlib import Path
import json, re, sys
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET
from urllib.robotparser import RobotFileParser

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

phase1_stems = (
    "guidebook-why-accurate-skin-diagnosis",
    "guidebook-accurate-skin-diagnosis-customer-trust",
    "guidebook-skin-analyzer-device-vs-software",
)
phase1_names = {f"{stem}-{locale}.html" for stem in phase1_stems for locale in expected_locales}
phase1_pages = [p for p in legacy_pages if p.name in phase1_names]
if {p.name for p in phase1_pages} != phase1_names:
    errors.append("phase 1 must include exactly the 12 approved legacy HTML pages")

class PageSignals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.lang = ""
        self.canonicals = []
        self.robots = []
        self.links = []
        self.refreshes = []
        self.scripts = []
        self.hreflangs = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "head": self.in_head = True
        if tag == "html": self.lang = attrs.get("lang", "")
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append((attrs.get("href"), self.in_head))
        if tag == "link" and "hreflang" in attrs:
            self.hreflangs.append(attrs.get("href", ""))
        if tag == "meta" and attrs.get("name", "").lower() in {"robots", "googlebot", "bingbot"}:
            self.robots.append((attrs.get("content", ""), self.in_head))
        if tag == "meta" and attrs.get("http-equiv", "").lower() == "refresh":
            self.refreshes.append(attrs)
        if tag == "script" and attrs.get("type") != "application/ld+json":
            self.scripts.append(attrs)
        if tag == "a" and not self.in_head:
            self.links.append((attrs.get("href", ""), attrs.get("rel", "")))

    def handle_endtag(self, tag):
        if tag == "head": self.in_head = False

pages_base = "https://choicedx-official.github.io/choicedx-ai-skin-diagnosis/"
phase1_urls = {pages_base + "outputs/" + name for name in phase1_names}
sitemap_urls = {e.text for e in ET.parse(ROOT / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
if phase1_urls & sitemap_urls:
    errors.append("phase 1 noindex URL is still in the sitemap")
robots_policy = RobotFileParser()
robots_policy.parse((ROOT / "robots.txt").read_text(encoding="utf-8").splitlines())

for p in phase1_pages:
    text = p.read_text(encoding="utf-8")
    signals = PageSignals()
    signals.feed(text)
    locale = p.stem.rsplit("-", 1)[1]
    official_base = "https://www.choicedx.com" + ("" if locale == "ko" else "/" + locale)
    is_product = "device-vs-software" in p.name
    expected = official_base + ("/product" if is_product else "/research")
    if signals.canonicals != [(expected, True)]:
        errors.append(f"phase 1 canonical must be unique, localized and in head: {p.name}")
    if len(signals.robots) != 1 or any(not in_head or {v.strip().lower() for v in value.split(",")} != {"noindex", "follow"} for value, in_head in signals.robots):
        errors.append(f"phase 1 requires one noindex, follow meta in head: {p.name}")
    if signals.lang != ("zh-CN" if locale == "zh" else locale):
        errors.append(f"phase 1 HTML language mismatch: {p.name}")
    if signals.refreshes or signals.scripts:
        errors.append(f"phase 1 must not automatically redirect: {p.name}")
    if (expected, "") not in signals.links:
        errors.append(f"visible followable official link missing: {p.name}")
    if is_product:
        for product in ("dx-smart", "dx-pico"):
            if (official_base + "/product/" + product, "") not in signals.links:
                errors.append(f"official {product} link missing: {p.name}")
    if any(urlsplit(url).hostname != "www.choicedx.com" for url in signals.hreflangs):
        errors.append(f"phase 1 hreflang points outside official site: {p.name}")
    for bot in ("Googlebot", "bingbot", "*"):
        if not robots_policy.can_fetch(bot, pages_base + "outputs/" + p.name):
            errors.append(f"robots.txt blocks phase 1 URL for {bot}: {p.name}")

# Catch links from any tracked HTML back into retired legacy URLs, including relative paths.
for p in ROOT.rglob("*.html"):
    signals = PageSignals()
    signals.feed(p.read_text(encoding="utf-8"))
    source_url = pages_base + p.relative_to(ROOT).as_posix()
    for href, _ in signals.links:
        resolved = urlsplit(urljoin(source_url, href))._replace(query="", fragment="").geturl()
        if resolved in phase1_urls:
            errors.append(f"internal link still targets phase 1 legacy URL: {p.relative_to(ROOT)} -> {href}")

remaining_redirects = [p for p in legacy_pages if p.name not in phase1_names]
for p in remaining_redirects:
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
# FAQ schema v2 stores its full localized Q&A in Markdown, not an items array.
faq_count = faq["canonical_question_count_per_language"]
question_ids = [qid for category in faq["categories"] for qid in category["question_ids"]]
if sorted(question_ids) != list(range(1, faq_count + 1)):
    errors.append("FAQ category question IDs must cover each canonical question once")
if set(faq["canonical_documents"]) != expected_locales:
    errors.append("FAQ canonical document locale mismatch")
for locale, rel in faq["canonical_documents"].items():
    document = ROOT / rel
    if not document.is_file():
        errors.append(f"missing FAQ canonical document: {rel}")
        continue
    numbers = re.findall(r"^### Q(\d+)\.", document.read_text(encoding="utf-8"), re.M)
    if [int(n) for n in numbers] != list(range(1, faq_count + 1)):
        errors.append(f"FAQ Markdown question count/order mismatch: {locale}")

if errors:
    print("VALIDATION FAILED")
    for e in errors:
        print("-",e)
    sys.exit(1)
print("VALIDATION PASSED")
print("Root:",ROOT)
print("Canonical FAQ questions per language:",faq_count)
print("Research participants:",research["study"]["participants"])
print("Phase 1 noindex notices:",len(phase1_pages))
print("Unchanged legacy permanent migrations:",len(remaining_redirects))
print("Entity intents:",len(entity_resolution["preferred_official_destinations"]))
