---
name: seo-audit
description: "Full website SEO audit with parallel subagent delegation. Detects business type, delegates to specialists, generates health score. Use when user says audit, full SEO check, analyze my site, or website health check."
user-invokable: true
argument-hint: "[url]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# Full Website SEO Audit

## Process

1. **Fetch homepage**: use `scripts/fetch_page.py` to retrieve HTML
2. **Detect business type**: analyze homepage signals (WordPress, publisher, SaaS, etc.)
3. **Crawl site**: follow internal links up to 500 pages, respect robots.txt
4. **Delegate to subagents** (parallel when possible, sequential fallback):
   - `seo-technical` -- robots.txt, sitemaps, canonicals, Core Web Vitals, security headers
   - `seo-content` -- E-E-A-T, readability, thin content, AI citation readiness
   - `seo-schema` -- detection, validation, generation recommendations
   - `seo-performance` -- LCP, INP, CLS measurements
   - `seo-visual` -- screenshots, mobile testing, above-fold analysis
   - `seo-geo` -- AI crawler access, llms.txt, citability, brand mention signals
   - `seo-wordpress` -- WordPress-specific audit via REST API (spawn when WordPress detected: wp-content, wp-json signals)
   - `seo-cluster` -- Semantic clustering analysis (spawn when blog/content strategy signals detected)
5. **Score** -- aggregate into SEO Health Score (0-100)
6. **Report** -- generate prioritized action plan

## Crawl Configuration

```
Max pages: 500
Respect robots.txt: Yes
Follow redirects: Yes (max 3 hops)
Timeout per page: 30 seconds
Concurrent requests: 5
Delay between requests: 1 second
```

## Output Files

- `FULL-AUDIT-REPORT.md`: Comprehensive findings
- `ACTION-PLAN.md`: Prioritized recommendations (Critical > High > Medium > Low)

## Scoring Weights

| Category | Weight |
|----------|--------|
| Technical SEO | 22% |
| Content Quality | 23% |
| On-Page SEO | 20% |
| Schema / Structured Data | 10% |
| Performance (CWV) | 10% |
| AI Search Readiness | 10% |
| Images | 5% |

## Report Structure

### Executive Summary
- Overall SEO Health Score (0-100)
- Business type detected
- Top 5 critical issues
- Top 5 quick wins

### Sections
- Technical SEO (crawlability, indexability, security, CWV)
- Content Quality (E-E-A-T, thin content, readability)
- On-Page SEO (titles, meta, headings, internal linking)
- Schema & Structured Data
- Performance (LCP, INP, CLS)
- Images (alt text, sizes, formats)
- AI Search Readiness (citability, GEO signals)
- WordPress Health (if WordPress detected)

## Priority Definitions

- **Critical**: Blocks indexing or causes penalties (fix immediately)
- **High**: Significantly impacts rankings (fix within 1 week)
- **Medium**: Optimization opportunity (fix within 1 month)
- **Low**: Nice to have (backlog)

## Error Handling

| Scenario | Action |
|----------|--------|
| URL unreachable | Report error. Suggest user verify URL. |
| robots.txt blocks | Analyze accessible pages only. Note limitation. |
| Rate limiting (429) | Back off, reduce concurrent requests. Report partial results. |
| Large sites (500+) | Cap crawl. Report findings for pages crawled. |
