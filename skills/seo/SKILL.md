---
name: seo
description: "SEO Blogger Toolkit - Complete blog content lifecycle: research topics, plan clusters, write articles, audit content, optimize for AI search, publish to WordPress. Triggers on: SEO, audit, blog, article, write, publish, WordPress, cluster, E-E-A-T, GEO, schema."
user-invokable: true
argument-hint: "[command] [url|keyword]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# SEO Blogger Toolkit - Orchestrator

**Invocation:** `/seo <command> <argument>`

Toolkit SEO complet pour blogueurs WordPress. 15 skills couvrant le cycle de vie
complet du contenu : recherche, planification, redaction, audit, optimisation IA, publication.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo-audit <url>` | Full website audit with parallel subagents |
| `/seo-wordpress <url>` | WordPress blog SEO audit via REST API |
| `/seo-wp-strategy <url>` | Content strategy, editorial calendar, gap analysis |
| `/seo-write-article <keyword>` | Write a full SEO + GEO optimized article |
| `/seo-outline-article <keyword>` | Plan article structure (H1-H3, key points) |
| `/seo-wordpress-publish <file>` | Publish article to WordPress via REST API |
| `/seo-brand-voice` | Define or check brand voice & editorial tone |
| `/seo-cluster <seed-keyword>` | Topic clusters: pillar + secondary articles |
| `/seo-content <url>` | E-E-A-T and content quality analysis |
| `/seo-page <url>` | Deep single-page SEO analysis |
| `/seo-schema <url>` | Detect, validate, generate Schema.org markup |
| `/seo-geo <url>` | AI search / GEO optimization (ChatGPT, Perplexity) |
| `/seo-images <url>` | Image optimization analysis |
| `/seo-technical <url>` | Technical SEO audit (CWV, mobile, crawlers) |

## Blogger Workflow

The recommended workflow for bloggers:

```
1. /seo-wordpress <url>          → Audit existing content
2. /seo-cluster <keyword>        → Plan pillar + secondary articles
3. /seo-wp-strategy <url>        → Generate 12-week editorial calendar
4. /seo-brand-voice              → Define writing tone & guidelines
5. /seo-outline-article <keyword> → Plan article structure
6. /seo-write-article <keyword>  → Write full article (SEO + GEO)
7. /seo-content <draft>          → Audit E-E-A-T before publish
8. /seo-schema <url>             → Add BlogPosting schema
9. /seo-geo <url>                → Optimize for AI citations
10. /seo-wordpress-publish <file> → Publish to WordPress
```

## Orchestration Logic

When `/seo-audit` is invoked:
1. Detect if site is WordPress (wp-content/wp-json signals)
2. Spawn core subagents: seo-technical, seo-content, seo-schema, seo-performance, seo-visual, seo-geo
3. If WordPress detected, also spawn seo-wordpress agent
4. If blog/content strategy signals detected, also spawn seo-cluster agent
5. Collect results and generate unified report with SEO Health Score (0-100)
6. Create prioritized action plan (Critical > High > Medium > Low)

## Industry Detection

Detect business type from homepage signals:
- **WordPress Blog**: wp-content, wp-includes, wp-json → auto-suggest `/seo-wordpress`
- **Publisher**: /blog, /articles, article schema, author pages
- **SaaS**: pricing page, /features, "free trial"
- **E-commerce**: /products, /cart, product schema
- **Local Service**: phone, address, Google Maps embed

## Quality Gates

- Never recommend HowTo schema (deprecated Sept 2023)
- FAQ schema: only gov/health sites for Google rich results
- All Core Web Vitals use INP, never FID
- Blog posts: minimum 1500 words for adequate coverage
- Pillar articles: minimum 3000 words

## Reference Files

Load on-demand (NOT at startup):
- `references/cwv-thresholds.md`: Core Web Vitals thresholds
- `references/schema-types.md`: Schema types with deprecation status
- `references/eeat-framework.md`: E-E-A-T evaluation criteria
- `references/quality-gates.md`: Content length minimums

## Sub-Skills (15)

1. **seo-audit** -- Full website audit with parallel agents
2. **seo-wordpress** -- WordPress blog SEO via REST API
3. **seo-wp-strategy** -- Content strategy & editorial calendar
4. **seo-write-article** -- AI-assisted article writing
5. **seo-outline-article** -- Article structure planning
6. **seo-wordpress-publish** -- Publish to WordPress
7. **seo-brand-voice** -- Brand voice & editorial guidelines
8. **seo-cluster** -- Topic clusters (pillar + secondaries)
9. **seo-content** -- E-E-A-T and content quality
10. **seo-page** -- Deep single-page analysis
11. **seo-schema** -- Schema markup
12. **seo-geo** -- AI search / GEO optimization
13. **seo-images** -- Image optimization
14. **seo-technical** -- Technical SEO

## Subagents

For parallel analysis during audits:
- `seo-technical` -- Crawlability, indexability, security, CWV
- `seo-content` -- E-E-A-T, readability, thin content
- `seo-schema` -- Detection, validation, generation
- `seo-performance` -- Core Web Vitals measurement
- `seo-visual` -- Screenshots, mobile testing
- `seo-geo` -- AI crawler access, citability
- `seo-wordpress` -- WordPress-specific audit (conditional: WP detected)
- `seo-cluster` -- Semantic clustering (conditional: blog detected)

## Error Handling

| Scenario | Action |
|----------|--------|
| Unrecognized command | List available commands. Suggest closest match. |
| URL unreachable | Report error. Suggest user verify URL. |
| Sub-skill fails | Report partial results. Note which failed and why. |
