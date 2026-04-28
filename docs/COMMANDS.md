# Commands Reference

## Overview

SEO Blogger Toolkit provides 14 commands for WordPress bloggers. All commands use the `/seo-xxx` format.

**Author:** Abderrahim KHALID (MEDIA BUYING ACADEMY) - https://mediabuying.ac/

## Command List

### `/seo-audit <url>`

Full website SEO audit with parallel analysis.

**Example:**
```
/seo-audit https://example.com
```

**What it does:**
1. Crawls site pages
2. Detects business type
3. Delegates to 8 specialist subagents in parallel
4. Generates SEO Health Score (0-100)
5. Creates prioritized action plan

**Output:**
- `FULL-AUDIT-REPORT.md`
- `ACTION-PLAN.md`
- `screenshots/` (if Playwright available)

---

### `/seo-wordpress <url>`

WordPress blog SEO audit via REST API.

**Example:**
```
/seo-wordpress https://myblog.com
```

**What it analyzes:**
- WordPress REST API configuration
- Permalink structure and URL patterns
- Post/page SEO metadata
- Plugin detection (Yoast, RankMath)
- Sitemap and robots.txt
- Content structure and categories

---

### `/seo-wp-strategy <url>`

Blog content strategy and editorial calendar.

**Example:**
```
/seo-wp-strategy https://myblog.com
```

**What it creates:**
- Content gap analysis
- Topic cluster planning
- Editorial calendar with priorities
- Content recommendations based on existing posts

---

### `/seo-write-article <keyword>`

AI-assisted article writing optimized for SEO and GEO.

**Example:**
```
/seo-write-article "best project management tools 2026"
```

**What it does:**
- Researches the topic and SERP landscape
- Writes a complete SEO-optimized article
- Includes E-E-A-T signals
- Optimizes for AI search citation (GEO)
- Generates meta title, description, schema markup

---

### `/seo-outline-article <keyword>`

Article structure planning before writing.

**Example:**
```
/seo-outline-article "remote work productivity tips"
```

**What it produces:**
- H1-H3 heading structure
- Key points per section
- Source recommendations
- Word count targets
- Internal linking opportunities

---

### `/seo-wordpress-publish <file>`

Publish an article to WordPress via REST API.

**Example:**
```
/seo-wordpress-publish article.md
```

**What it does:**
- Converts markdown to WordPress-compatible HTML
- Publishes via REST API with Application Password auth
- Sets categories, tags, featured image
- Configures SEO metadata (Yoast/RankMath)
- Supports draft and publish modes

---

### `/seo-brand-voice`

Define or check brand voice and editorial guidelines.

**Example:**
```
/seo-brand-voice
```

**What it does:**
- Guides you through brand voice definition
- Creates editorial guidelines document
- Checks content against established voice
- Ensures consistency across articles

---

### `/seo-cluster <seed-keyword>`

Semantic topic clustering with pillar and secondary articles.

**Example:**
```
/seo-cluster "email marketing"
```

**What it creates:**
- Pillar article definition
- Secondary article clusters
- Hub-and-spoke internal linking plan
- Content priorities and sequencing

---

### `/seo-content <url>`

E-E-A-T and content quality analysis.

**Example:**
```
/seo-content https://example.com/blog/post
```

**What it evaluates:**
- Experience signals (first-hand knowledge)
- Expertise (author credentials)
- Authoritativeness (external recognition)
- Trustworthiness (transparency, security)
- AI citation readiness
- Content freshness

---

### `/seo-page <url>`

Deep single-page analysis.

**Example:**
```
/seo-page https://example.com/about
```

**What it analyzes:**
- On-page SEO (title, meta, headings, URLs)
- Content quality (word count, readability, E-E-A-T)
- Technical elements (canonical, robots, Open Graph)
- Schema markup
- Images (alt text, sizes, formats)
- Core Web Vitals potential issues

---

### `/seo-schema <url>`

Schema markup detection, validation, and generation.

**Example:**
```
/seo-schema https://example.com
```

**What it does:**
- Detects existing schema (JSON-LD, Microdata, RDFa)
- Validates against Google's requirements
- Identifies missing opportunities
- Generates ready-to-use JSON-LD

---

### `/seo-geo <url>`

AI Overviews / Generative Engine Optimization.

**Example:**
```
/seo-geo https://example.com/blog/guide
```

**What it analyzes:**
- Citability score (quotable facts, statistics)
- Structural readability (headings, lists, tables)
- Entity clarity (definitions, context)
- Authority signals (credentials, sources)
- Structured data support
- AI search readiness (ChatGPT, Perplexity, Google AI Overviews)

---

### `/seo-images <url>`

Image optimization analysis.

**Example:**
```
/seo-images https://example.com
```

**What it checks:**
- Alt text presence and quality
- File sizes (flag >200KB)
- Formats (WebP/AVIF recommendations)
- Responsive images (srcset, sizes)
- Lazy loading
- CLS prevention (dimensions)

---

### `/seo-technical <url>`

Technical SEO audit across 9 categories.

**Example:**
```
/seo-technical https://example.com
```

**Categories:**
1. Crawlability
2. Indexability
3. Security
4. URL Structure
5. Mobile Optimization
6. Core Web Vitals (LCP, INP, CLS)
7. Structured Data
8. JavaScript Rendering
9. IndexNow Protocol

---

## Quick Reference

| Command | Use Case |
|---------|----------|
| `/seo-audit <url>` | Full website audit |
| `/seo-wordpress <url>` | WordPress blog SEO audit |
| `/seo-wp-strategy <url>` | Content strategy & editorial calendar |
| `/seo-write-article <keyword>` | AI-assisted article writing |
| `/seo-outline-article <keyword>` | Article structure planning |
| `/seo-wordpress-publish <file>` | Publish to WordPress |
| `/seo-brand-voice` | Brand voice & editorial guidelines |
| `/seo-cluster <seed-keyword>` | Topic clusters (pillar + secondary) |
| `/seo-content <url>` | E-E-A-T analysis |
| `/seo-page <url>` | Single page analysis |
| `/seo-schema <url>` | Schema validation & generation |
| `/seo-geo <url>` | AI search optimization |
| `/seo-images <url>` | Image optimization |
| `/seo-technical <url>` | Technical SEO check |

## Extension Commands

Extensions add additional commands when installed:

| Command | Extension | Description |
|---------|-----------|-------------|
| `/seo-dataforseo [command]` | DataForSEO | Live SERP, keywords, backlinks, AI visibility |
| `/seo-image-gen [use-case] <desc>` | Banana | AI image generation via Gemini |
| `/seo-firecrawl [command]` | Firecrawl | Advanced web scraping and crawling |
