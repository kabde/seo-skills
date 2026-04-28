---
name: seo-wp-strategy
description: >
  Content strategy generator for WordPress bloggers. Creates editorial calendars,
  topic cluster plans, content gap analysis, and growth roadmaps based on existing
  WordPress content audit. Use when user says "content strategy", "editorial calendar",
  "blog strategy", "topic clusters", "content plan", or "que publier".
user-invokable: true
argument-hint: "<wordpress-url> [--user username] [--password app-password]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# WordPress Blog Content Strategy

## Invocation

`/seo-wp-strategy <url>`

## Prerequisites

Same as `seo-wordpress`: WordPress site with REST API + Application Password.

## Workflow

### Phase 1: Content Inventory

Run the WordPress audit first:
```bash
python scripts/wordpress_api.py <url> --user <user> --password <pass> --command seo-audit --json
python scripts/wp_content_analyzer.py <url> --user <user> --password <pass> --command full --json
```

Collect:
- All posts with word counts, dates, categories, tags
- Topic clusters from categories
- Content freshness data
- Internal linking health
- E-E-A-T signals

### Phase 2: Gap Analysis

Based on the content inventory, identify:

1. **Thin clusters**: Categories with < 5 articles
2. **Missing pillar content**: Clusters without a 3000+ word cornerstone article
3. **Orphan content**: Articles not linked to/from other content
4. **Stale content**: Articles not updated in 12+ months
5. **Missing formats**: No how-to guides, listicles, case studies, comparisons
6. **Keyword gaps**: Topics mentioned but not covered in dedicated articles

### Phase 3: Competitor Quick-Scan

If user provides competitor URLs:
- Compare post volume per category
- Identify topics competitors cover that user doesn't
- Note content formats competitors use

### Phase 4: Strategy Generation

#### Topic Cluster Architecture

For each existing category, propose:
- **Pillar article** (3000+ words, comprehensive guide)
- **Cluster articles** (1500+ words each, specific subtopics)
- **Supporting content** (listicles, how-tos, FAQs)
- **Internal linking plan** (hub-and-spoke model)

#### Editorial Calendar

Generate a 12-week content calendar with REAL data:

**Rules for calendar generation:**
1. Calculate real start dates from today's date (e.g., Week 1 = next Monday)
2. Generate REAL article titles based on cluster analysis and SERP research
3. Assign REAL categories from the WordPress site
4. Include target keywords for each article
5. Estimate writing time (pillar: 8-12h, cluster: 4-6h, supporting: 2-3h)

**Example output format (with real data):**

| Week | Start Date | Article Title | Type | Category | Target Keyword | Words | Est. Time | Priority |
|------|------------|---------------|------|----------|----------------|-------|-----------|----------|
| 1 | 2026-04-29 | Guide Complet du SEO WordPress en 2026 | Pillar | SEO | seo wordpress | 3000+ | 10h | Critical |
| 2 | 2026-05-06 | Comment Installer Yoast SEO Etape par Etape | How-to | SEO | installer yoast seo | 1500+ | 5h | High |
| 3 | 2026-05-13 | 10 Plugins WordPress Indispensables pour le SEO | Listicle | SEO | plugins seo wordpress | 1500+ | 4h | High |
| 4 | 2026-05-20 | Yoast vs RankMath : Quel Plugin SEO Choisir ? | Comparison | SEO | yoast vs rankmath | 1500+ | 5h | Medium |

**Dependencies:** Pillar articles MUST be published before their cluster articles.

Priority rules:
- **Week 1-4**: Fix critical issues (update stale pillar content, add missing meta) + publish first pillar
- **Week 5-8**: Strengthen weak clusters (new cluster articles around the pillar)
- **Week 9-12**: Expand into new topic areas, second pillar

**After generating calendar, suggest:**
- `/seo-outline-article <keyword>` for each article in the calendar
- `/seo-write-article <keyword>` to start writing

#### Content Types Mix

Recommend a healthy content mix:
| Type | Percentage | Purpose |
|------|-----------|---------|
| Pillar/Guide | 15% | Authority building, SEO cornerstone |
| How-to | 25% | Search intent capture, experience signals |
| Listicle | 20% | Engagement, shareability |
| Case study | 15% | E-E-A-T experience, trust |
| Opinion/Analysis | 10% | Expertise signals, thought leadership |
| Comparison | 10% | Commercial intent, decision stage |
| News/Update | 5% | Freshness signals |

#### Update Plan

For existing content:
1. Articles > 12 months old: refresh data, update examples, add new sections
2. Articles < 1500 words: expand with more detail, examples, images
3. Articles with 0 internal links: add 3-5 relevant links
4. Articles without images: add 2-3 relevant images with alt text

## Output Format

### Blog Strategy Report

#### Current State Summary
- Total articles: X
- Average word count: X
- Topic clusters: X (X healthy, X weak)
- Content freshness score: X%
- Internal linking score: X%

#### Top 5 Quick Wins
1. [Specific action on specific post]
2. ...

#### 12-Week Editorial Calendar
[Table format]

#### Topic Cluster Plan
[Visual cluster map per category]

#### Content Update Queue
[Prioritized list of existing articles to update]

#### Growth Projections
Based on consistent publishing (2 articles/week):
- Month 1: Foundation (update existing, fill gaps)
- Month 2-3: Cluster building (strengthen 2-3 main topics)
- Month 4-6: Authority (pillar content, link building readiness)

## Cross-Skill Integration

- Use `/seo-cluster <keyword>` to validate topic cluster with SERP data
- Use `/seo-content <url>` to deep-dive specific articles before updating
- Use `/seo-geo <url>` to optimize for AI search citations
- Use `/seo-schema <url>` to add BlogPosting schema

## Error Handling

| Scenario | Action |
|----------|--------|
| < 5 posts on site | Focus on initial content plan rather than gap analysis |
| No categories used | Recommend taxonomy setup before content strategy |
| All content stale | Prioritize update plan over new content |
| No SEO plugin | Include plugin setup as Week 0 prerequisite |
