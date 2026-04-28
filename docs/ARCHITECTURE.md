# Architecture

## Overview

SEO Blogger Toolkit is a modular Claude Code skill suite built for WordPress bloggers. It follows Anthropic's official skill specification with 15 skills, 8 subagents, 10 scripts, and 3 optional extensions.

**Author:** Abderrahim KHALID (MEDIA BUYING ACADEMY) - https://mediabuying.ac/
**Version:** 1.0.0

## Directory Structure

```
claude-seo/
├── skills/                            # 15 skills
│   ├── seo/                           # Main orchestrator
│   │   ├── SKILL.md                       # Entry point with routing logic
│   │   └── references/                    # On-demand reference files
│   │       ├── cwv-thresholds.md
│   │       ├── schema-types.md
│   │       ├── eeat-framework.md
│   │       └── quality-gates.md
│   │
│   ├── seo-audit/SKILL.md                # Full site audit with parallel agents
│   ├── seo-wordpress/                     # WordPress blog SEO via REST API
│   │   ├── SKILL.md
│   │   └── references/
│   ├── seo-wp-strategy/SKILL.md          # Blog content strategy & editorial calendar
│   ├── seo-write-article/SKILL.md        # AI-assisted article writing (SEO + GEO)
│   ├── seo-outline-article/SKILL.md      # Article structure planning
│   ├── seo-wordpress-publish/SKILL.md    # Publish to WordPress via REST API
│   ├── seo-brand-voice/SKILL.md          # Brand voice & editorial guidelines
│   ├── seo-cluster/                       # Semantic topic clustering
│   │   ├── SKILL.md
│   │   ├── references/
│   │   └── templates/
│   ├── seo-content/SKILL.md              # E-E-A-T and content quality
│   ├── seo-page/SKILL.md                 # Deep single-page analysis
│   ├── seo-schema/SKILL.md              # Schema.org markup
│   ├── seo-geo/SKILL.md                 # AI search / GEO optimization
│   ├── seo-images/SKILL.md              # Image optimization
│   └── seo-technical/SKILL.md           # Technical SEO
│
├── agents/                            # 8 subagents
│   ├── seo-technical.md                  # Technical SEO specialist
│   ├── seo-content.md                    # Content quality reviewer
│   ├── seo-schema.md                     # Schema markup expert
│   ├── seo-performance.md                # Performance analyzer
│   ├── seo-visual.md                     # Visual analyzer
│   ├── seo-geo.md                        # GEO / AI search specialist
│   ├── seo-wordpress.md                  # WordPress audit specialist
│   └── seo-cluster.md                    # Topic cluster architect
│
├── scripts/                           # 10 Python scripts
│   ├── wordpress_api.py                  # WordPress REST API (read + write + publish)
│   ├── wp_content_analyzer.py            # Content deep analyzer (readability, clusters, E-E-A-T)
│   ├── georeadiness_analyzer.py          # GEO/AI citation readiness scorer
│   ├── llms_txt_generator.py             # llms.txt generator for WordPress
│   ├── fetch_page.py                     # Page fetcher with UA rotation
│   ├── parse_html.py                     # HTML parser for SEO elements
│   ├── pagespeed_check.py                # PageSpeed Insights v5 + CrUX API
│   ├── google_report.py                  # PDF/HTML report generator
│   ├── capture_screenshot.py             # Playwright screenshots
│   └── analyze_visual.py                 # Visual analysis helper
│
├── hooks/
│   ├── hooks.json                        # PostToolUse schema validation
│   └── validate-schema.py
│
├── schema/                            # Schema.org JSON-LD templates
│
├── extensions/                        # 3 optional extensions
│   ├── banana/                           # Banana Image Generation (Gemini AI)
│   ├── dataforseo/                       # DataForSEO MCP integration
│   └── firecrawl/                        # Firecrawl web scraping MCP
│
└── docs/                              # Documentation
```

## Component Types

### Skills

Skills are markdown files with YAML frontmatter that define capabilities and instructions.

**SKILL.md Format:**
```yaml
---
name: skill-name
description: >
  When to use this skill. Include activation keywords
  and concrete use cases.
---

# Skill Title

Instructions and documentation...
```

### Subagents

Subagents are specialized workers that can be delegated tasks. They have their own context and tools.

**Agent Format:**
```yaml
---
name: agent-name
description: What this agent does.
tools: Read, Bash, Write, Glob, Grep
---

Instructions for the agent...
```

### Reference Files

Reference files contain static data loaded on-demand to avoid bloating the main skill.

### Scripts

Python scripts (stdlib + minimal dependencies) provide data fetching, parsing, and analysis. All scripts include CLI interface and JSON output.

## Orchestration Flow

### Full Audit (`/seo-audit`)

```
User Request
    │
    ▼
┌─────────────────┐
│   seo-audit     │  ← Audit orchestrator
│   (SKILL.md)    │
└────────┬────────┘
         │
         │  Detects business type
         │  Spawns subagents in parallel
         │
    ┌────┴────┬────────┬────────┬────────┬────────┬────────┬────────┐
    ▼         ▼        ▼        ▼        ▼        ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│tech   │ │content│ │schema │ │perf   │ │visual │ │geo    │ │word-  │ │cluster│
│agent  │ │agent  │ │agent  │ │agent  │ │agent  │ │agent  │ │press  │ │agent  │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │        │        │        │        │        │        │
    └─────────┴────────┴────┬───┴────────┴────────┴────────┴────────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Aggregate    │
                    │  Results      │
                    └───────┬───────┘
                            │
                            ▼
                    ┌───────────────┐
                    │  Generate     │
                    │  Report       │
                    └───────────────┘
```

### Individual Command

```
User Request (e.g., /seo-page)
    │
    ▼
┌─────────────────┐
│   seo           │  ← Routes to sub-skill
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   seo-page      │  ← Sub-skill handles directly
│   (SKILL.md)    │
└─────────────────┘
```

## Design Principles

### 1. Blogger-First

Every skill serves the blog content lifecycle: research, write, audit, publish. WordPress REST API integration is native throughout.

### 2. Progressive Disclosure

- Main SKILL.md is concise (<500 lines)
- Reference files loaded on-demand
- Detailed instructions in sub-skills

### 3. Parallel Processing

- Subagents run concurrently during audits
- Independent analyses don't block each other
- Results aggregated after all complete

### 4. AI-Ready

- GEO optimization for ChatGPT, Perplexity, Google AI Overviews
- Citability scoring and entity clarity analysis
- llms.txt generation for AI discoverability

### 5. Quality Gates

- Built-in thresholds prevent bad recommendations
- Schema deprecation awareness
- FID replaced by INP enforcement

## Skill Overview

| Skill | Description |
|-------|-------------|
| `seo` | Main orchestrator, routes commands |
| `seo-audit` | Full site audit with parallel agents |
| `seo-wordpress` | WordPress blog SEO via REST API |
| `seo-wp-strategy` | Blog content strategy & editorial calendar |
| `seo-write-article` | AI-assisted article writing (SEO + GEO) |
| `seo-outline-article` | Article structure planning |
| `seo-wordpress-publish` | Publish to WordPress via REST API |
| `seo-brand-voice` | Brand voice & editorial guidelines |
| `seo-cluster` | Semantic topic clustering (pillar + secondary) |
| `seo-content` | E-E-A-T and content quality analysis |
| `seo-page` | Deep single-page analysis |
| `seo-schema` | Schema.org detection, validation, generation |
| `seo-geo` | AI search / GEO optimization |
| `seo-images` | Image optimization analysis |
| `seo-technical` | Technical SEO audit |

## Agent Overview

| Agent | Role |
|-------|------|
| `seo-technical` | Technical SEO specialist |
| `seo-content` | Content quality reviewer |
| `seo-schema` | Schema markup expert |
| `seo-performance` | Performance analyzer |
| `seo-visual` | Visual analyzer |
| `seo-geo` | GEO / AI search specialist |
| `seo-wordpress` | WordPress audit specialist |
| `seo-cluster` | Topic cluster architect |

## File Naming Conventions

| Type | Pattern | Example |
|------|---------|---------|
| Skill | `seo-{name}/SKILL.md` | `seo-audit/SKILL.md` |
| Agent | `seo-{name}.md` | `seo-technical.md` |
| Reference | `{topic}.md` | `cwv-thresholds.md` |
| Script | `{action}_{target}.py` | `fetch_page.py` |
| Template | `{name}.md` | `pillar-template.md` |

## Extension Points

### Adding a New Sub-Skill

1. Create `skills/seo-newskill/SKILL.md`
2. Add YAML frontmatter with name and description
3. Write skill instructions
4. Update main `skills/seo/SKILL.md` to route to new skill

### Adding a New Subagent

1. Create `agents/seo-newagent.md`
2. Add YAML frontmatter with name, description, tools
3. Write agent instructions
4. Reference from relevant skills

### Adding a New Reference File

1. Create file in appropriate `references/` directory
2. Reference in skill with load-on-demand instruction

## Extensions

Extensions are opt-in add-ons that integrate external data sources via MCP servers. They live in `extensions/<name>/` and include their own install/uninstall scripts.

```
extensions/
├── banana/                   # Banana Image Generation (Gemini AI)
│   ├── README.md
│   ├── install.sh / uninstall.sh
│   ├── skills/
│   │   └── seo-image-gen/SKILL.md
│   ├── agents/
│   │   └── seo-image-gen.md
│   ├── scripts/
│   ├── references/
│   └── docs/
│       └── BANANA-SETUP.md
│
├── dataforseo/               # DataForSEO MCP integration
│   ├── README.md
│   ├── install.sh / uninstall.sh
│   ├── field-config.json
│   ├── skills/
│   │   └── seo-dataforseo/SKILL.md
│   ├── agents/
│   │   └── seo-dataforseo.md
│   └── docs/
│       └── DATAFORSEO-SETUP.md
│
└── firecrawl/                # Firecrawl web scraping MCP
    ├── README.md
    ├── install.sh / uninstall.sh
    ├── skills/
    │   └── seo-firecrawl/SKILL.md
    └── docs/
        └── FIRECRAWL-SETUP.md
```

### Available Extensions

| Extension | Package | What it Adds |
|-----------|---------|-------------|
| **Banana Image Gen** | `@ycse/nanobanana-mcp` | AI image generation for SEO assets via Gemini AI |
| **DataForSEO** | `dataforseo-mcp-server` | Live SERP, keywords, backlinks, on-page analysis, AI visibility |
| **Firecrawl** | Firecrawl MCP | Advanced web scraping and crawling for deep site analysis |

### Extension Convention

Each extension follows this pattern:
1. Self-contained in `extensions/<name>/`
2. Own `install.sh` that copies files and configures MCP
3. Own `uninstall.sh` that cleanly reverses installation
4. Installs skill to `~/.claude/skills/seo-<name>/`
5. Installs agent to `~/.claude/agents/seo-<name>.md` (if applicable)
6. Merges MCP config into `~/.claude/settings.json` (non-destructive)
