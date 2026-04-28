---
name: seo-write-article
description: >
  AI-assisted SEO article writer. Generates full blog articles optimized for Google
  and AI search engines (ChatGPT, Perplexity, AI Overviews). Supports templates:
  how-to, listicle, guide, comparison, case study, explainer. Integrates E-E-A-T
  signals, GEO citability, and internal linking. Use when user says "write article",
  "rediger", "draft", "create post", or "write blog".
user-invokable: true
argument-hint: "<keyword> [--template how-to|listicle|guide|comparison|case-study|explainer] [--tone expert|friendly|formal]"
license: MIT
metadata:
  author: Abderrahim KHALID (MEDIA BUYING ACADEMY)
  version: "1.0.0"
  category: seo
---

# SEO Article Writer

## Invocation

`/seo-write-article <keyword>`

Optional flags:
- `--template <type>` : how-to, listicle, guide, comparison, case-study, explainer (default: auto-detect)
- `--tone <tone>` : expert, friendly, formal (default: from brand voice or friendly)
- `--words <count>` : target word count (default: 1800 for standard, 3500 for pillar)
- `--audience <segment>` : target reader persona (default: from brand voice)
- `--cluster <name>` : link to an existing cluster plan for internal linking

## Prerequisites

1. **Brand voice profile** (optional): `brand-voice.md` in project root or `~/.config/claude-seo/brand-voice.md`
2. **Cluster context** (optional): if the article belongs to a topic cluster, pass `--cluster` to load the cluster plan for internal linking
3. **WebSearch access**: required for SERP research and PAA questions

## Input Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| keyword | Yes | - | Primary target keyword |
| template | No | auto | Article structure template |
| tone | No | friendly | Writing tone/style |
| words | No | 1800 | Target word count |
| audience | No | general | Target reader persona |
| cluster | No | - | Cluster plan name for internal links |

## Workflow

### Step 1: Keyword Research

Use WebSearch to gather:
- Top 10 Google SERP results for the target keyword
- People Also Ask (PAA) questions (aim for 5-8)
- Related searches and long-tail variations
- Current featured snippet format (paragraph, list, table)

Store results for outline generation and content gap analysis.

### Step 2: Load Brand Voice Profile

If `brand-voice.md` exists, load:
- Tone and style guidelines
- Vocabulary preferences (words to use / avoid)
- Sentence structure preferences
- Brand-specific terminology
- Target audience description

If no profile exists, use the `--tone` flag or default to friendly-expert.

### Step 3: Load Cluster Context

If `--cluster` is specified:
- Load the cluster plan from `clusters/<name>/cluster-plan.md`
- Identify the current article's role (pillar or secondary)
- Extract internal linking targets (other articles in the cluster)
- Note the pillar page URL for linking back

### Step 4: Generate Article Outline

Build the heading structure:
- **H1**: Main title (incorporate primary keyword naturally)
- **H2s**: 5-8 main sections covering the topic comprehensively
- **H3s**: Subsections where depth is needed
- Include PAA questions as H2/H3 headings where relevant
- Plan GEO citability block placement (2-3 sections)

Present outline to user for approval before writing.

### Step 5: Write Each Section

For each section:
- Open with a hook or context sentence
- Cover key points with depth and specificity
- Use transition sentences between paragraphs
- Incorporate keywords naturally (no stuffing)
- Add data points, statistics, or examples where relevant
- Maintain the chosen tone throughout

### Step 6: Add GEO-Optimized Passages

Insert 2-3 **citability blocks** throughout the article:
- Each block is 134-167 words (optimal for AI citation)
- Self-contained: makes sense without surrounding context
- Uses definition patterns: "X is...", "X refers to..."
- Includes specific data, numbers, or step sequences
- Positioned after relevant H2 headings
- Marked with an HTML comment `<!-- citability-block -->` for tracking

Example citability block pattern:
```
[Term] is [clear definition]. [Specific detail with number/data].
[How it works or why it matters]. [Practical implication].
[Additional context that rounds out the answer].
```

### Step 7: Insert Internal Links

From the cluster plan or site context:
- Link to pillar page (if this is a secondary article)
- Link to 2-4 related secondary articles
- Use descriptive anchor text (not "click here")
- Place links naturally within relevant paragraphs
- Minimum 3 internal links per article

### Step 8: Add E-E-A-T Signals

Integrate throughout the article:

**Experience markers:**
- First-person insights: "In our testing...", "When we implemented..."
- Specific results: "This increased traffic by 34%..."
- Process documentation: "Here's the exact workflow we used..."

**Expertise markers:**
- Technical accuracy with proper terminology
- Nuanced explanations that go beyond surface level
- References to industry standards or frameworks

**Authority signals:**
- Citations to authoritative sources (studies, official docs)
- Links to original research or data
- Reference to recognized methodologies

**Trust signals:**
- Date of writing/last update
- Clear author attribution
- Transparent methodology disclosure

### Step 9: Generate Meta Tags

**Meta title** (30-60 characters):
- Include primary keyword near the beginning
- Add a benefit or modifier
- Stay within character limit

**Meta description** (120-160 characters):
- Summarize the article's value proposition
- Include primary keyword naturally
- Add a call-to-action or hook
- Stay within character limit

### Step 10: Suggest Featured Image Alt Text

Generate descriptive alt text that:
- Describes the image concept relevant to the article
- Includes the primary keyword naturally
- Is under 125 characters
- Provides real value for accessibility

### Step 11: Output Complete Article

Deliver the article in Markdown with YAML frontmatter:

```markdown
---
title: "Meta Title Here"
description: "Meta description here"
category: "Category"
tags: ["tag1", "tag2", "tag3"]
featured_image_alt: "Descriptive alt text"
date: "YYYY-MM-DD"
author: "Author Name"
word_count: 1800
template: "how-to"
cluster: "cluster-name"
---

# H1 Title

Article content...
```

## Article Templates

### How-To Template
```
H1: How to [Action] [Result/Benefit]
H2: What Is [Topic] (and Why It Matters)
H2: What You'll Need / Prerequisites
H2: Step 1: [First Action]
  H3: [Sub-step if needed]
H2: Step 2: [Second Action]
H2: Step 3: [Third Action]
H2: Common Mistakes to Avoid
H2: FAQ (from PAA questions)
H2: Key Takeaways
```

### Listicle Template
```
H1: [Number] [Adjective] [Topic] for [Audience/Goal]
H2: 1. [Item Name]
  H3: Why It Works / Key Features
  H3: Best For
H2: 2. [Item Name]
...
H2: How to Choose the Right [Topic]
H2: FAQ
```

### Guide Template
```
H1: The Complete Guide to [Topic] ([Year])
H2: What Is [Topic]?
H2: Why [Topic] Matters
H2: [Core Concept 1]
  H3: [Detail A]
  H3: [Detail B]
H2: [Core Concept 2]
H2: [Core Concept 3]
H2: Advanced Tips
H2: Tools and Resources
H2: FAQ
```

### Comparison Template
```
H1: [Option A] vs [Option B]: [Differentiator] ([Year])
H2: Quick Comparison Table
H2: What Is [Option A]?
H2: What Is [Option B]?
H2: [Criteria 1] Comparison
H2: [Criteria 2] Comparison
H2: [Criteria 3] Comparison
H2: Which Should You Choose?
H2: FAQ
```

### Case Study Template
```
H1: How [Subject] Achieved [Result] with [Method]
H2: The Challenge / The Approach / The Results
H2: Key Lessons Learned / How to Apply This
H2: FAQ
```

### Explainer Template
```
H1: What Is [Topic]? Everything You Need to Know
H2: [Topic] Definition / How It Works
H2: Types / Benefits / Challenges
H2: Examples / How to Get Started / FAQ
```

## Quality Checks

Before delivering the article, verify:

| Check | Standard Article | Pillar Article |
|-------|-----------------|----------------|
| Word count | >= 1,500 | >= 3,000 |
| H2 headings | >= 3 | >= 6 |
| H3 headings | >= 2 | >= 5 |
| Internal links | >= 3 | >= 6 |
| External links | >= 2 | >= 4 |
| Images with alt text | >= 1 | >= 3 |
| Citability blocks | >= 2 | >= 3 |
| Meta title length | 30-60 chars | 30-60 chars |
| Meta description | 120-160 chars | 120-160 chars |
| Keyword in H1 | Yes | Yes |
| Keyword in first 100 words | Yes | Yes |
| FAQ section | Recommended | Required |

## Cross-Skill Integration

After writing the article:
- Run `/seo-content` to audit content quality and E-E-A-T score
- Run `/seo-schema` to generate Article schema markup
- Run `/seo-wordpress-publish` to publish directly to WordPress
- Run `/seo-images` to optimize any referenced images
- Run `/seo-geo` to verify GEO/AI citation readiness
