---
name: seo-outline-article
description: >
  Article structure planner. Analyzes top SERP results and generates detailed article
  outlines with H1-H3 hierarchy, word count targets per section, key points, sources,
  and internal linking opportunities. Use when user says "outline", "plan article",
  "article structure", or "plan de contenu".
user-invokable: true
argument-hint: "<keyword> [--type standard|pillar] [--template how-to|listicle|guide|comparison|case-study|explainer]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# Article Outline Planner

## Invocation

`/seo-outline-article <keyword>`

Optional flags:
- `--type <type>` : standard or pillar (default: standard)
- `--template <template>` : how-to, listicle, guide, comparison, case-study, explainer (default: auto-detect from SERP)
- `--cluster <name>` : load cluster plan for internal link suggestions

## Prerequisites

1. **WebSearch access**: required for SERP analysis and competitor research
2. **Cluster context** (optional): pass `--cluster` to integrate with an existing topic cluster

## Workflow

### Step 1: Keyword Research

Use WebSearch to collect:
- Top 10 Google SERP results for the target keyword
- People Also Ask (PAA) questions (5-8 questions)
- Related searches and long-tail keyword variations
- Featured snippet format currently ranking (paragraph, list, table)
- Search intent classification (informational, commercial, transactional, navigational)

### Step 2: Analyze Competitor Outlines

For each top 5 ranking page:
- Extract heading structure (H1, H2, H3)
- Estimate word count per section
- Note content formats used (lists, tables, images, videos)
- Identify unique angles or data points
- Record external sources cited

Build a **competitor heading matrix**:

```
| Heading Topic        | Page 1 | Page 2 | Page 3 | Page 4 | Page 5 |
|----------------------|--------|--------|--------|--------|--------|
| Definition/What Is   |   Y    |   Y    |   Y    |   Y    |   Y    |
| How It Works         |   Y    |   Y    |   N    |   Y    |   N    |
| Benefits             |   Y    |   N    |   Y    |   Y    |   Y    |
| [Topic-specific]     |   N    |   Y    |   N    |   N    |   N    |
```

### Step 3: Identify Content Gaps

From the competitor analysis, find:
- **Topics all competitors cover** (must include - table stakes)
- **Topics most competitors miss** (opportunity for differentiation)
- **Questions from PAA not answered** by top results
- **Depth gaps**: sections competitors cover superficially
- **Format gaps**: content types competitors don't use (tables, comparisons, calculators)
- **Freshness gaps**: outdated data or stats in competitor articles

### Step 4: Generate the Outline

Produce a detailed outline with:

**H1 - Main Title (3 variants)**
Provide 3 title options incorporating the primary keyword:
1. Direct/clear variant
2. Benefit-driven variant
3. Curiosity/number-driven variant

**H2 Sections**
- Standard article: 5-8 H2 sections
- Pillar article: 8-12 H2 sections

For each H2:
- Heading text (with keyword integration where natural)
- Word count target (150-400 words per section)
- Key points to cover (3-5 bullet points)
- Sources to reference (URLs from research)
- Whether this section gets a GEO citability block

**H3 Subsections**
- Add H3s where a section needs structured depth
- Each H3: heading text + 2-3 key points + word count target

**GEO Citability Block Placement**
Mark 2-3 sections where a citability block (134-167 words) should be written:
- Typically the definition/overview section
- A key process or methodology section
- A summary or comparison section

**Internal Link Suggestions**
From cluster context or site knowledge:
- Which existing articles to link to
- Suggested anchor text for each link
- Where in the outline each link fits naturally

### Step 5: Competitor Comparison Table

Generate a summary table showing your planned outline vs competitors:

```
| Section               | Competitors | Your Outline | Your Advantage        |
|-----------------------|-------------|--------------|----------------------|
| Definition            | 5/5 cover   | Included     | + GEO citability block|
| Step-by-step process  | 3/5 cover   | Included     | + Screenshots/examples|
| Common mistakes       | 1/5 cover   | Included     | Content gap win       |
| Tool comparison       | 0/5 cover   | Included     | Unique angle          |
| FAQ                   | 2/5 cover   | Included     | + PAA questions       |
```

## Output Format

The outline is delivered as a Markdown file:

```markdown
---
keyword: "target keyword"
search_intent: "informational"
template: "how-to"
type: "standard"
target_word_count: 2000
estimated_sections: 7
geo_citability_blocks: 3
date_planned: "YYYY-MM-DD"
---

# Article Outline: [Keyword]

## Title Options
1. [Direct title variant]
2. [Benefit-driven title variant]
3. [Curiosity/number-driven title variant]

## Search Intent & SERP Analysis
- **Intent**: Informational
- **Featured snippet**: List format
- **PAA questions**: [list]
- **Top competitor word counts**: [range]

## Outline

### H2: [Section Title] (~250 words)
**Key points:**
- Point 1
- Point 2
- Point 3

**Sources:** [URL1], [URL2]
**Internal link:** [anchor text] -> [target article]
**GEO block:** Yes - definition pattern

### H2: [Section Title] (~300 words)
...

## Content Gap Opportunities
- [Gap 1]: [Why it matters]
- [Gap 2]: [Why it matters]

## Competitor Comparison
| Section | Coverage | Your Edge |
|---------|----------|-----------|
| ...     | ...      | ...       |

## Internal Linking Plan
- Link 1: [anchor] -> [URL] (in Section X)
- Link 2: [anchor] -> [URL] (in Section Y)
- Link 3: [anchor] -> [URL] (in Section Z)
```

## Outline Quality Checks

| Check | Standard | Pillar |
|-------|----------|--------|
| H2 sections | 5-8 | 8-12 |
| H3 subsections | 2+ | 5+ |
| Title variants | 3 | 3 |
| PAA questions addressed | 3+ | 5+ |
| Content gaps identified | 2+ | 4+ |
| Internal links planned | 3+ | 6+ |
| GEO blocks planned | 2 | 3 |
| Word count target | 1,500-2,500 | 3,000-5,000 |
| Sources per section | 1+ | 2+ |

## Cross-Skill Integration

After generating the outline:
- Run `/seo-write-article <keyword>` to write the full article from this outline
- Run `/seo-cluster` if the keyword should be part of a topic cluster
- Run `/seo-geo` to check GEO readiness of planned citability blocks
