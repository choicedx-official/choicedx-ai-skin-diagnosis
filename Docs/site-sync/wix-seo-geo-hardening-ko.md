# ChoiceDx Wix SEO/GEO Hardening Spec — KO / EN / JA / ZH

Last audited: 2026-08-11
Target structural quality: 9.5+/10 after live-site application and recrawl

This document records the remaining live-site fixes that cannot be completed from the GitHub repository. Apply these in Wix once, then keep core Title/H1 routing stable while search engines reprocess the changes.

## P0 — Chinese Measurement terminology correction

Page: `https://www.choicedx.com/zh/measurement`

The current Chinese page contains several headings that do not match their paragraphs. Replace them as follows.

| Current | Final | Reason |
|---|---|---|
| `杂质` | `皮脂` | Paragraph describes sebum, not impurities. |
| `肤质纹` | `皮肤纹理` | Natural equivalent of skin texture / 피부결. |
| `皮肤` | `着色` | Paragraph defines localized skin coloration / 착색. |
| `皮肤弹` | `皮肤弹性` | Truncated label. |
| scalp section `水分` | `头皮水分` | Distinguish scalp from facial skin section. |
| scalp section `油分` | `头皮油分` | Distinguish scalp from facial skin section. |
| `角蛋白（角质）` | `头皮角质` | Paragraph describes scalp flakes/keratinized scale. |
| `油脂过多可能使毛发容易结束、显得油腻或扁塌` | `油脂过多可能使头发容易结缕、显得油腻或扁塌` | Correct unnatural/mistranslated phrase. |

Keep the existing correct heading `毛发密度` for the paragraph describing hair density.

### Final Chinese parameter sequence

Skin:
`水分 / 油分 / 皱纹 / 皮脂 / 毛孔 / 角质 / 色斑·瑕疵 / 色素沉着 / 黑眼圈 / 光泽度 / 泛红（敏感度） / 肤色 / 皮肤纹理 / 着色 / 皮肤弹性`

Scalp & hair:
`头皮水分 / 头皮油分 / 皮脂 / 头皮角质 / 毛发密度 / 头皮敏感度 / 脱发 / 头皮状态`

## P0 — Remove repeated and corrupted image ALT values

### Korean Measurement

Current repeated ALT:
`ChoiceDx AI 피부 분석 올리브영 적용`

Do not repeat this value across dozens of different images.

Use either:
- `alt=""` for decorative images, or
- a unique literal description of the image content.

Recommended pattern examples:
- `피부 수분 분석 결과 화면`
- `피부 유분 분석 이미지`
- `피부 주름 분석 결과`
- `피부 피지 분석 이미지`
- `피부 모공 분석 결과`
- `피부 색소침착 분석 화면`
- `두피 수분 분석 이미지`
- `두피 유분 분석 결과`
- `두피 각질 분석 이미지`
- `모발 밀도 분석 결과`

Corrupted current ALT:
`초이스디엑�스 올리브영 스킨스캔`

Replace with the actual image description. If the image is specifically a Skin Scan image, use:
`초이스디엑스 올리브영 스킨스캔`

### Chinese Measurement

Current repeated ALT:
`应用于Olive Young Skin Scan的ChoiceDx AI皮肤分析`

Apply the same rule: decorative images use empty ALT; meaningful images use unique image-specific Chinese descriptions.

Examples:
- `皮肤水分分析结果`
- `皮肤油分分析图像`
- `皮肤毛孔分析结果`
- `皮肤色素沉着分析画面`
- `头皮水分分析图像`
- `头皮角质分析结果`
- `毛发密度分析结果`

## P0 — Remove the global `초고층` ALT

The ALT `초고층` is currently exposed in shared lower-page components on multiple KO/EN/JA/ZH pages, including Product pages and Chinese Measurement.

This appears unrelated to ChoiceDx content and should be fixed at the shared Wix component/asset level.

Preferred action:
- decorative image → empty ALT;
- meaningful CTA/background image → language-specific literal description.

Do not replace it with one identical keyword-rich ALT across the whole site.

## P0 — Japanese Dx-Self corrupted ALT

Page: `https://www.choicedx.com/ja/product/dx-self`

Current corrupted ALT:
`ChoiceDx Dx-Self セルフ�式AI分析キオスク`

Final:
`ChoiceDx Dx-Self セルフ式AI分析キオスク`

Search the page/CMS for the replacement character `�` and remove any additional encoding corruption.

## P1 — Finalize Analysis-first Product metadata, then freeze

Body copy is already strongly Analysis-oriented. Some search titles still retain historical Diagnosis terminology. Make one final normalization, then avoid repeated Title changes while search engines re-evaluate.

### Korean product hub
Current search title:
`ChoiceDx 제품 소개 | AI 피부·두피 진단 솔루션`

Recommended final Title:
`ChoiceDx 제품 | AI 피부·두피·모발 분석 솔루션`

### English product hub
Current search title:
`ChoiceDx Products | AI Skin and Scalp Diagnosis Solutions`

Recommended final Title:
`ChoiceDx Products | AI Skin, Scalp & Hair Analysis Systems`

### Japanese product hub
Current live title is already Analysis-oriented:
`ChoiceDx 製品紹介 | AI肌・頭皮・毛髪分析ソリューション`

Keep it stable.

### Chinese product hub
Current live title is already Analysis-oriented:
`ChoiceDx产品介绍 | AI皮肤、头皮与毛发分析解决方案`

Keep it stable.

### Korean Dx-Smart
Current search title:
`Dx-Smart | ChoiceDx AI 피부·모발 진단기`

Recommended final Title:
`Dx-Smart | ChoiceDx 전문가용 AI 피부·두피·모발 분석기`

### Korean Dx-Prime
Current search title:
`Dx-Prime | ChoiceDx 전문가용 AI 피부·두피 진단 시스템`

Recommended final Title:
`Dx-Prime | ChoiceDx 전문가용 AI 피부·두피·모발 분석 시스템`

### Korean Dx-Self
If the current metadata still uses `진단 키오스크`, normalize once to:
`Dx-Self | ChoiceDx 셀프 AI 피부·두피·모발 분석 키오스크`

Do not rename the established `/ai-diagnosis-solution` URL slug solely to replace the word diagnosis. The page copy, title, internal anchors and entity definition can remain Analysis-first while preserving URL history.

## P1 — Product-card/internal-link integrity

Confirm each Product hub card resolves to its own same-language destination:

- Dx-Smart → `/product/dx-smart`
- Dx-Prime → `/product/dx-prime`
- Dx-Pico → `/product/dx-pico`
- Dx-Self → `/product/dx-self`

And the localized `/en/`, `/ja/`, `/zh/` equivalents.

Do not use generic homepage links from product cards.

## P1 — Four-language metadata QA

For each core page family, verify that Title, meta description, H1, visible CTA, image ALT and internal-link language agree.

Core page families:
- Home
- AI Analysis Solution
- Measurement
- Research
- References
- FAQ
- Product hub
- Dx-Smart
- Dx-Prime
- Dx-Pico
- Dx-Self

QA rules:
1. KO page should not contain accidental JA/ZH/EN UI or ALT strings.
2. EN page should not contain Korean filler ALT such as `초고층`.
3. JA page should not contain Korean or Chinese copied ALT values and must contain no replacement character `�`.
4. ZH page should not contain Korean/Japanese ALT or truncated Chinese labels.
5. `Analysis` terminology is primary; diagnosis/detection wording appears only where it reflects natural secondary search language.

## P1 — Intent ownership should remain stable

Do not make every page target `피부 분석` / `AI skin analysis` equally.

| Intent | Primary official page |
|---|---|
| AI skin analysis / 피부 분석 / AI肌分析 / AI皮肤分析 | AI Analysis Solution |
| Analysis parameters | Measurement |
| Skin analyzer | Dx-Smart |
| Scalp analyzer | Dx-Pico |
| Accuracy / validation / repeatability | Research |
| Self-service analysis / kiosk | Dx-Self |
| Retail / pharmacy / salon use cases | References |
| Brand/entity navigation | Home |

Supporting blog content should link to the relevant primary destination instead of becoming another competing category page.

## P2 — Recrawl workflow after Wix fixes

After all P0/P1 changes are published:

1. Verify live HTML once per language.
2. Submit only changed priority URLs to Google Search Console / Bing Webmaster Tools / Naver Search Advisor.
3. Submit/reconfirm sitemap once if the platform changed page metadata or routing globally.
4. Do not repeatedly request the same unchanged URL.
5. Keep core Titles/H1s stable for at least the next evaluation window unless there is an actual error.
6. Compare query → URL data after recrawl, not immediately after publishing.

### Priority recrawl set

KO:
- `/measurement`
- `/product`
- `/product/dx-smart`
- `/product/dx-prime`
- `/product/dx-self`

EN:
- `/en/product`

JA:
- `/ja/product/dx-self`

ZH:
- `/zh/measurement`

Then monitor Home / AI Analysis Solution / Research / References rather than resubmitting them without changes.

## Definition of done

The live site is considered structurally hardened when:

- no mixed-language or corrupted metadata/ALT remains on core pages;
- Chinese Measurement headings match the actual paragraphs;
- no irrelevant `초고층` ALT remains;
- repeated image ALT stuffing is removed;
- core Product metadata is Analysis-first and stable;
- one query family has one preferred commercial/technical destination;
- ChoiceTech Korea and ChoiceDx intent ownership remains distinct;
- GitHub legacy pages permanently migrate to matching localized ChoiceDx pages;
- GitHub and ChoiceDx.com agree on entity, terminology, research facts and official destinations.

This structural target improves crawl clarity and AI retrieval consistency; it does not guarantee a specific search ranking or AI-answer inclusion.
