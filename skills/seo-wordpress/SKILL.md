---
name: seo-wordpress
description: >
  WordPress SEO audit via REST API with Application Password. Analyzes posts,
  pages, categories, tags, media, internal linking, SEO plugin meta (Yoast/RankMath),
  content depth, and schema markup. Use when user says "wordpress", "wp audit",
  "blog audit", "analyse wordpress", "contenu wordpress", or provides a WordPress URL.
user-invokable: true
argument-hint: "<wordpress-url> [--user username] [--password app-password]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# WordPress SEO Analysis

## Invocation

`/seo-wordpress <url>`

## Prerequisites

1. **WordPress site** with REST API enabled (default since WP 4.7+)
2. **Application Password** for authenticated access (Settings > Users > Application Passwords)
3. Credentials stored at `~/.config/claude-seo/wordpress.json`:

```json
{
  "sites": {
    "example.com": {
      "url": "https://example.com",
      "username": "admin",
      "app_password": "xxxx xxxx xxxx xxxx"
    }
  }
}
```

## Workflow

### Step 1: WordPress Detection

Run: `python scripts/wordpress_api.py <url> --check --json`

Verify:
- WordPress is detected (`is_wordpress: true`)
- REST API is available (`api_available: true`)
- Identify SEO plugin (Yoast, RankMath, AIOSEO, or none)

If no SEO plugin detected, flag as **Critical** issue.

### Step 2: Credential Loading

Check for stored credentials:
```bash
python scripts/wordpress_api.py <url> --user <user> --password <pass> --command info --json
```

If no credentials provided, ask the user:
1. WordPress username
2. Application Password (Settings > Users > Application Passwords in WP admin)

### Step 3: Full Content Audit

Run: `python scripts/wordpress_api.py <url> --user <user> --password <pass> --command seo-audit --json`

This analyzes:
- **All published posts**: word count, headings, images, links, meta
- **All published pages**: same analysis
- **Categories**: descriptions, hierarchy, post counts
- **Tags**: usage, relevance
- **Media**: alt text, file sizes
- **Internal linking**: orphan detection, link matrix

### Step 4: SEO Plugin Meta Analysis

Run: `python scripts/wordpress_api.py <url> --user <user> --password <pass> --command seo-meta --json`

Extracts:
- SEO titles and meta descriptions
- Canonical URLs
- Open Graph data
- Schema markup per post
- Focus keywords (RankMath)
- Robots directives

### Step 5: Internal Linking Analysis

Run: `python scripts/wordpress_api.py <url> --user <user> --password <pass> --command linking-matrix --json`

Identifies:
- Orphan pages (no incoming links)
- Dead-end pages (no outgoing links)
- Link distribution imbalance
- Cluster connectivity gaps

## Analysis Criteria

### Content Depth (per post)

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| Word count | 1500+ | 800-1499 | <800 |
| H2 headings | 3+ | 1-2 | 0 |
| Images | 2+ with alt | 1+ partial alt | 0 or no alt |
| Internal links | 3+ | 1-2 | 0 |
| External links | 1+ | 0 | N/A |
| Meta description | Set, 120-160 chars | Set but wrong length | Missing |

### Blog-Specific E-E-A-T

| Signal | What to Check |
|--------|---------------|
| Experience | Author bio, personal anecdotes in content, original photos |
| Expertise | Author credentials, technical depth, accurate claims |
| Authoritativeness | Author pages exist, external citations |
| Trustworthiness | Contact page, about page, privacy policy, HTTPS |

### WordPress-Specific Technical SEO

| Check | Good | Issue |
|-------|------|-------|
| Permalink structure | /%postname%/ | Default ?p=123 |
| XML sitemap | Auto-generated (WP 5.5+) or plugin | Missing |
| Robots.txt | Properly configured | Blocking important content |
| SEO plugin | Yoast or RankMath active | No SEO plugin |
| Image sizes | WebP/AVIF, <200KB | Unoptimized PNG/JPG >500KB |
| Caching | Cache plugin detected | No caching |
| Schema | BlogPosting/Article on posts | Missing structured data |

### Category/Tag Taxonomy

| Check | Good | Issue |
|-------|------|-------|
| Category descriptions | All have descriptions | Empty descriptions |
| Category hierarchy | Organized parent/child | Flat structure |
| Empty categories | All have 2+ posts | Categories with 0 posts |
| Tag relevance | Tags used 3+ times | Tags used only once |
| Tag/Category overlap | Distinct purposes | Duplicate tags and categories |

## Output Format

### WordPress SEO Score: XX/100

### Site Overview
| Metric | Value |
|--------|-------|
| Posts | X |
| Pages | X |
| Categories | X |
| Tags | X |
| SEO Plugin | Yoast/RankMath/None |

### Score Breakdown
| Area | Score | Details |
|------|-------|---------|
| Content Depth | XX% | X posts meet 1500+ word threshold |
| Meta Optimization | XX% | X posts have SEO title + description |
| Internal Linking | XX% | X posts have 3+ internal links |
| Image Optimization | XX% | X posts have optimized images |
| Taxonomy Health | XX% | Categories and tags properly used |

### Issues (prioritized)
- **Critical**: [list]
- **High**: [list]
- **Medium**: [list]
- **Low**: [list]

### Top 10 Recommendations
1. [Actionable recommendation with specific post/page]
2. ...

### Content Calendar Suggestions
Based on category gaps and thin content, suggest:
- Articles to update/expand
- New articles to write (fill topic gaps)
- Categories to strengthen

## Cross-Skill Integration

After WordPress audit, suggest:
- `/seo-technical <url>` for deeper technical analysis
- `/seo-content <url>` for E-E-A-T deep dive on specific posts
- `/seo-schema <url>` for structured data optimization
- `/seo-cluster <keyword>` for topic cluster planning
- `/seo-geo <url>` for AI search readiness
- `/seo-wp-strategy` for full content strategy

## Error Handling

| Scenario | Action |
|----------|--------|
| Not a WordPress site | Report detection failure, suggest `/seo-audit` instead |
| API disabled | Suggest enabling REST API or using Application Password |
| Auth failed (401) | Guide user through Application Password setup |
| No SEO plugin | Flag as critical, recommend Yoast or RankMath installation |
| Rate limited | Wait and retry with exponential backoff |
| Empty site (<5 posts) | Suggest `/seo-wp-strategy` for content planning first |
