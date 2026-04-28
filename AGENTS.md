# SEO Blogger Toolkit — Multi-Platform Agent Instructions

> For **Cursor**, **Cursor Cloud Agents**, **Google Antigravity**, and **Gemini CLI**.
> Claude Code users: see `CLAUDE.md` instead.

## Overview

SEO Blogger Toolkit v1.0.0 — 15 skills pour le cycle de vie complet du contenu blog
WordPress : audit, strategie, redaction, publication, optimisation SEO et IA.

## Quick Reference

| Command | What it does |
|---------|-------------|
| `/seo-audit <url>` | Full website audit with parallel subagents |
| `/seo-wordpress <url>` | WordPress blog SEO audit via REST API |
| `/seo-wp-strategy <url>` | Content strategy & editorial calendar |
| `/seo-write-article <keyword>` | AI-assisted article writing (SEO + GEO) |
| `/seo-outline-article <keyword>` | Article structure planning (H1-H3) |
| `/seo-wordpress-publish <file>` | Publish article to WordPress |
| `/seo-brand-voice` | Define or check brand voice & tone |
| `/seo-cluster <keyword>` | Topic clusters: pillar + secondary articles |
| `/seo-content <url>` | E-E-A-T and content quality analysis |
| `/seo-page <url>` | Deep single-page SEO analysis |
| `/seo-schema <url>` | Schema.org detection, validation, generation |
| `/seo-geo <url>` | AI search / GEO optimization |
| `/seo-images <url>` | Image optimization analysis |
| `/seo-technical <url>` | Technical SEO audit (CWV, mobile, crawlers) |

## Blogger Workflow

```
1. /seo-wordpress        → Audit existing WordPress content
2. /seo-cluster          → Plan pillar + secondary articles
3. /seo-wp-strategy      → Generate 12-week editorial calendar
4. /seo-brand-voice      → Define writing tone & guidelines
5. /seo-outline-article  → Plan article structure
6. /seo-write-article    → Write full article (SEO + GEO)
7. /seo-content          → Audit E-E-A-T before publish
8. /seo-schema           → Add BlogPosting schema
9. /seo-geo              → Optimize for AI citations
10. /seo-wordpress-publish → Publish to WordPress
```

## Using with Cursor / Cursor Cloud

Cursor reads this file automatically. All SKILL.md files contain the full
analysis logic as natural language instructions. Python scripts in `scripts/`
provide execution capabilities.

**Running scripts directly:**
```bash
# WordPress audit
python scripts/wordpress_api.py https://example.com --check --json

# Content analysis
python scripts/wp_content_analyzer.py https://example.com --user admin --password xxxx --json

# GEO readiness check
python scripts/georeadiness_analyzer.py https://example.com --json

# Generate llms.txt
python scripts/llms_txt_generator.py https://example.com --user admin --password xxxx

# Page fetching
python scripts/fetch_page.py https://example.com

# HTML parsing for SEO elements
python scripts/parse_html.py page.html --json
```

**Cursor Cloud gotchas:**
- SSL certificates may not resolve for some domains — investigate rather than disabling verification
- PATH may not include Python venv — use full path: `~/.claude/skills/seo/.venv/bin/python`
- Screenshots save to `/tmp/` not CWD — check absolute paths

## Using with Google Antigravity

Antigravity discovers this project via `plugin.json` at the repo root.
Place the repo in `~/.gemini/antigravity/plugins/claude-seo/` or install via:

```bash
bash install.sh
```

## Architecture

```
skills/                    # 15 skills
  seo/SKILL.md            # Main orchestrator + routing
  seo-audit/              # Full site audit
  seo-wordpress/          # WordPress REST API audit
  seo-wp-strategy/        # Content strategy & calendar
  seo-write-article/      # Article writing
  seo-outline-article/    # Article outline planning
  seo-wordpress-publish/  # WordPress publishing
  seo-brand-voice/        # Brand voice & tone
  seo-cluster/            # Topic clustering (pillar + spokes)
  seo-content/            # E-E-A-T quality analysis
  seo-page/               # Single-page analysis
  seo-schema/             # Schema.org markup
  seo-geo/                # AI search / GEO
  seo-images/             # Image optimization
  seo-technical/          # Technical SEO
agents/                    # 8 subagents
scripts/                   # 10 Python scripts
schema/                    # JSON-LD templates (BlogPosting, BreadcrumbList)
extensions/                # Optional: DataForSEO, Firecrawl, Banana
```

## Key Principles

1. **Blogger-First**: Every skill serves the blog content lifecycle
2. **WordPress Native**: REST API integration with Application Password
3. **AI-Ready**: GEO optimization for ChatGPT, Perplexity, Google AI Overviews
4. **Security**: All scripts call `validate_url()` for SSRF protection
5. **Config location**: `~/.config/claude-seo/wordpress.json` for credentials

## Credits

Created by **Abderrahim KHALID** — [MEDIA BUYING ACADEMY](https://mediabuying.ac/)
