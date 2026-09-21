#!/usr/bin/env python3
"""Validate the curated sitemap, reciprocal language links and shared product facts."""
import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
import xml.etree.ElementTree as ET

from validate_markdown_pages import BASE, ROOT, frontmatter, output_path


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_head = False
        self.alternates = []
        self.links = []
        self.current_links = []
        self.canonicals = []
        self.robots = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'head':
            self.in_head = True
        if tag == 'link' and 'hreflang' in a:
            self.alternates.append((a['hreflang'], a.get('href'), self.in_head))
        if tag == 'link' and 'canonical' in a.get('rel', '').split():
            self.canonicals.append(a.get('href'))
        if tag == 'meta' and a.get('name', '').lower() in ('robots', 'googlebot', 'bingbot'):
            self.robots.append(a.get('content', '').lower())
        if tag == 'a':
            self.links.append(a.get('href', ''))
            if a.get('aria-current') == 'page':
                self.current_links.append(a.get('href'))

    def handle_endtag(self, tag):
        if tag == 'head':
            self.in_head = False


def read(path):
    return (ROOT / path).read_text(encoding='utf-8')


def check_product_counts(check):
    products = json.loads(read('data/products.json'))['products']
    # Extract counts from the named product paragraph, never observation magnification.
    patterns = {
        'ko': (r'피부\s*(?:최대\s*)?(\d+)개', r'모발·두피\s*(?:최대\s*)?(\d+)개'),
        'en': (r'(\d+) skin parameters', r'(\d+) (?:hair/scalp|scalp/hair) metrics'),
        'ja': (r'肌(?:最大)?(\d+)項目', r'毛髪・頭皮(?:最大)?(\d+)項目'),
        'zh': (r'(\d+)项皮肤指标', r'(\d+)项毛发/头皮指标'),
    }

    def compare(text, locale, expected, label):
        actual = []
        for pattern in patterns[locale]:
            matches = re.findall(pattern, text)
            actual.append(int(matches[0]) if len(matches) == 1 else None)
        check(tuple(actual) == expected, f'{label}: count pair {actual} differs from products.json {expected}')

    llms = read('llms-full.txt')
    for product in products[:4]:
        name = product['name']
        facts = product['official_page_summary']
        expected = (facts.get('skin_parameters_up_to', facts.get('skin_parameters')),
                    facts.get('scalp_hair_metrics_up_to', facts.get('scalp_hair_metrics')))
        for locale in patterns:
            guide = read(f'Docs/products/product-guide-{locale}.md')
            paragraphs = [p for p in guide.split('\n\n') if p.startswith(name) and not p.startswith(name + 'の')]
            check(len(paragraphs) == 1, f'{locale}/{name}: expected one product paragraph')
            if len(paragraphs) == 1:
                compare(paragraphs[0], locale, expected, f'product-guide-{locale}/{name}')
            if name in ('Dx-Smart', 'Dx-Pico'):
                question = 16 if name == 'Dx-Smart' else 18
                faq = read(f'Docs/faq/faq-v2-{locale}.md')
                answer = re.search(rf'^### Q{question}\..*?\n(.*?)(?=\n### Q|\Z)', faq, re.M | re.S)
                check(answer is not None, f'faq-v2-{locale}: Q{question} missing')
                if answer:
                    compare(answer[1], locale, expected, f'faq-v2-{locale}/{name}')
        line = re.search(rf'^{re.escape(name)}: (.+)$', llms, re.M)
        check(line is not None, f'llms-full.txt: {name} summary missing')
        if line:
            compare(line[1], 'en', expected, f'llms-full.txt/{name}')
    smart = products[0]
    check(smart.get('observation_confirmation_status') == 'internal_product_specification_confirmation_required',
          'Dx-Smart conflicting observation specifications require internal confirmation')
    check(smart.get('observation_source_locale') == 'ko' and 'Japanese: 10x / 30x' in smart.get('observation_verification_note', '')
          and 'Chinese: 20x / 30x' in smart.get('observation_verification_note', ''),
          'Keep source-specific Dx-Smart observation discrepancy evidence')


def validate(site=None):
    errors = []
    def check(condition, message):
        if not condition:
            errors.append(message)

    config = json.loads(read('_data/document_discovery.json'))
    groups = config['groups']
    check({g['key'] for g in groups} == {'faq', 'measurement', 'use-cases'}, 'Unexpected promoted document families')
    expected_alternates = {}
    index = read('Docs/README.md')
    for group in groups:
        pages = group['pages']
        check(len(pages) == 4 and {p['hreflang'] for p in pages} == {'ko', 'en', 'ja', 'zh-Hans'}, f'{group["key"]}: four language versions required')
        alternates = [(p['hreflang'], BASE.rstrip('/') + p['path'], True) for p in pages]
        for page in pages:
            source = page['source']
            check(source not in expected_alternates, f'{source}: duplicate language group membership')
            expected_alternates[source] = alternates
            front = frontmatter(read(source))
            check(front.get('translation_key') == group['key'], f'{source}: translation group mismatch')
            check('noindex' not in front.get('robots', ''), f'{source}: noindex must not enter language set')
            check('canonical_url' not in front, f'{source}: language set must retain self-canonical')
            check(page['path'] == '/' + output_path(Path(source)).as_posix(), f'{source}: URL differs from Jekyll output')
            check('](' + BASE.rstrip('/') + page['path'] + ')' in index, f'{source}: clickable index link missing')
    check(len(expected_alternates) == 12, 'Expected 12 promoted localized documents')

    paths = config['sitemap_paths']
    check(len(paths) == len(set(paths)) == 25, 'Expected 25 unique curated sitemap URLs')
    sitemap_urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    expected_urls = [BASE.rstrip('/') + path for path in paths]
    check(sitemap_urls == expected_urls, 'Sitemap differs from curated canonical URL list')
    docs = [p for p in ROOT.rglob('*.md') if not any(part.startswith(('.', '_')) for part in p.relative_to(ROOT).parts) and p.relative_to(ROOT).as_posix() != 'outputs/README.md']
    rendered_pages = {}
    for source in docs:
        rel = source.relative_to(ROOT)
        front = frontmatter(source.read_text(encoding='utf-8'))
        path = '/' + output_path(rel).as_posix()
        if path.endswith('index.html'):
            path = path[:-len('index.html')]
        check(('translation_key' in front) == (rel.as_posix() in expected_alternates), f'{rel}: unexpected language-alternate membership')
        if 'noindex' in front.get('robots', '') or 'choicedx-faq-knowledge-base-' in rel.name:
            check(path not in paths, f'{rel}: noindex/compatibility URL must not be in curated sitemap')
        if site:
            html = site / output_path(rel)
            check(html.is_file(), f'{rel}: generated page missing')
            if not html.is_file():
                continue
            page = Page(); page.feed(html.read_text(encoding='utf-8'))
            rendered_pages[path] = page
            check(page.alternates == expected_alternates.get(rel.as_posix(), []), f'{rel}: unexpected or missing reciprocal hreflang')
            if rel.as_posix() in expected_alternates:
                resolved = [urljoin(BASE + output_path(rel).as_posix(), href) for href in page.links]
                check(all(url in resolved for _, url, _ in expected_alternates[rel.as_posix()]), f'{rel}: visible alternate links missing')
                check(BASE + 'Docs/' in resolved, f'{rel}: documentation index link missing')
                check([urljoin(BASE, link) for link in page.current_links] == [BASE.rstrip('/') + path], f'{rel}: current language marker incorrect')
    if site:
        for path, url in zip(paths, expected_urls):
            if path in rendered_pages:
                page = rendered_pages[path]
            else:
                html = site / path.lstrip('/')
                check(html.is_file(), f'{path}: sitemap target missing')
                if not html.is_file():
                    continue
                page = Page(); page.feed(html.read_text(encoding='utf-8'))
            check(page.canonicals == [url], f'{path}: sitemap URL is not its rendered canonical')
            check(not any('noindex' in value for value in page.robots), f'{path}: sitemap target is noindex')
        for source in ('Docs/index.html', 'Docs/faq/index.html'):
            page = Page(); page.feed((site / source).read_text(encoding='utf-8'))
            for href in page.links:
                url = urljoin(BASE + source, href)
                if url.startswith(BASE):
                    path = urlsplit(url).path[len(urlsplit(BASE).path):]
                    target = site / path
                    if urlsplit(url).path.endswith('/'):
                        target /= 'index.html'
                    check(target.is_file(), f'{source}: broken local navigation {href}')
    check_product_counts(check)
    if errors:
        raise SystemExit('\n'.join(errors))
    print('PASS: 12 pages in 3 reciprocal language groups, 25 eligible sitemap URLs, 28 product count references' + ('; rendered navigation and canonical targets' if site else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=Path)
    args = parser.parse_args()
    validate(args.site.resolve() if args.site else None)
