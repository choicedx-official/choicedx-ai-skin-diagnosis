#!/usr/bin/env python3
"""Check the bounded Markdown SEO policy, including actual Jekyll output."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://choicedx-official.github.io/choicedx-ai-skin-diagnosis/'
LANGS = {'ko': 'ko-KR', 'en': 'en', 'ja': 'ja', 'zh': 'zh-CN'}
TARGETS = {
    f'Docs/{folder}/{stem}-{locale}.md'
    for folder, stem in [('research', 'research-validation'), ('products', 'product-guide')]
    for locale in LANGS
}


def frontmatter(text):
    match = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not match:
        return {}
    return dict(re.findall(r'^([a-z_]+):\s*(.+)$', match[1], re.M))


def output_path(path):
    return path.with_name('index.html') if path.name == 'README.md' else path.with_suffix('.html')


class Signals(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.canonicals = []
        self.robots = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'link' and 'canonical' in attrs.get('rel', '').split():
            self.canonicals.append(attrs.get('href'))
        if tag == 'meta' and attrs.get('name', '').lower() in ('robots', 'googlebot', 'bingbot'):
            self.robots.append(attrs.get('content', '').lower())
        if tag == 'a':
            self.links.append(attrs.get('href'))


def validate(site=None):
    errors = []
    def check(ok, message):
        if not ok:
            errors.append(message)

    docs = [p for p in ROOT.rglob('*.md') if not any(part.startswith(('.', '_')) for part in p.relative_to(ROOT).parts) and p.relative_to(ROOT).as_posix() != 'outputs/README.md']
    check(len(docs) == 48, f'Expected 48 published Markdown documents, found {len(docs)}')
    noindex = set()
    localized = 0
    for path in docs:
        rel = path.relative_to(ROOT)
        name = rel.as_posix()
        body = path.read_text(encoding='utf-8')
        front = frontmatter(body)
        locale = re.search(r'-(ko|en|ja|zh)\.md$', name)
        # This operational note is English prose despite its historical -ko filename.
        is_localized = locale and name != 'Docs/site-sync/wix-seo-geo-hardening-ko.md'
        expected_lang = LANGS[locale[1]] if is_localized else 'en-US'
        if is_localized:
            localized += 1
            check(front.get('lang') == expected_lang, f'{name}: incorrect lang')
            check(front.get('language') == expected_lang, f'{name}: language metadata differs')
        if 'noindex' in front.get('robots', ''):
            noindex.add(name)
        research = name.startswith('Docs/research/research-validation-')
        rendered = output_path(rel)
        self_canonical = BASE + rendered.as_posix()
        if self_canonical.endswith('index.html'):
            self_canonical = self_canonical[:-len('index.html')]
        expected_canonical = ('https://www.choicedx.com/' + ('' if locale[1] == 'ko' else locale[1] + '/') + 'research') if research else self_canonical
        if name in TARGETS:
            check(front.get('robots') == 'noindex, follow', f'{name}: incorrect robots')
        if research:
            check(front.get('canonical_url') == expected_canonical, f'{name}: incorrect Research canonical')
            check(f']({expected_canonical})' in body, f'{name}: visible Research link missing')
        else:
            check('canonical_url' not in front, f'{name}: preserve generated self-canonical')
        if site:
            html_path = site / rendered
            check(html_path.is_file(), f'{rendered}: missing Jekyll output')
            if not html_path.is_file():
                continue
            html = html_path.read_text(encoding='utf-8')
            page = Signals()
            page.feed(html)
            check(page.lang == expected_lang, f'{rendered}: html lang {page.lang!r} != {expected_lang!r}')
            check(page.canonicals == [expected_canonical], f'{rendered}: canonical {page.canonicals!r}')
            check(page.robots == (['noindex, follow'] if name in TARGETS else []), f'{rendered}: unexpected robots {page.robots!r}')
            if research:
                check(expected_canonical in page.links, f'{rendered}: Research link missing')
            check('{{ page.' not in html, f'{rendered}: Liquid was not rendered')
    check(localized == 32, f'Expected 32 localized Markdown sources, found {localized}')
    check(noindex == TARGETS, f'Only the approved 8 documents may have noindex: {noindex ^ TARGETS}')
    layout = (ROOT / '_layouts/default.html').read_text(encoding='utf-8')
    check('page.lang | default: site.lang | default: "en-US"' in layout, 'Language precedence changed')
    check(layout.count('{% seo %}') == 1, 'Use one SEO tag for one canonical')
    products = json.loads((ROOT / 'data/products.json').read_text(encoding='utf-8'))['products']
    for product, expected in zip(products[:4], [(10, 9), (10, 9), (10, 10), (9, 8)]):
        data = product['official_page_summary']
        actual = (data.get('skin_parameters_up_to', data.get('skin_parameters')), data.get('scalp_hair_metrics_up_to', data.get('scalp_hair_metrics')))
        check(actual == expected, f'{product["name"]}: verified parameter counts changed')
    if site:
        # Phase 1 HTML and the other static Evidence/legacy pages bypass this layout.
        for source in list((ROOT / 'outputs').glob('*.html')) + [ROOT / 'robots.txt', ROOT / 'sitemap.xml']:
            rendered = site / source.relative_to(ROOT)
            check(rendered.is_file() and source.read_bytes() == rendered.read_bytes(), f'{source.name}: static content changed during rendering')
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: 48 Markdown documents; exactly 8 noindex and 40 preserved; 32 localized sources; canonical and product policies' + ('; rendered HTML and 35 static files' if site else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path)
    args = parser.parse_args()
    validate(args.site.resolve() if args.site else None)
