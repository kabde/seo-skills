# SEO Blogger Toolkit - Claude Code Skills

## Project Overview

**SEO Blogger Toolkit** pour blogueurs WordPress. 15 skills couvrant l'audit WordPress
via REST API, la redaction assistee d'articles SEO, la publication WordPress, les topic
clusters (pillar + secondaires), l'analyse E-E-A-T, le schema markup, l'optimisation
images, le SEO technique, et le referencement sur les moteurs IA (ChatGPT, Perplexity,
Google AI Overviews).

## Architecture

```
claude-seo/
  CLAUDE.md                          # Project instructions (this file)
  .claude-plugin/
    plugin.json                    # Plugin manifest
    marketplace.json               # Marketplace catalog
  skills/                            # 15 skills
    seo/                           # Main orchestrator
      SKILL.md
      references/                  # On-demand knowledge files
    seo-audit/SKILL.md            # Full site audit with parallel agents
    seo-wordpress/                 # WordPress blog SEO via REST API
      SKILL.md
      references/
    seo-wp-strategy/SKILL.md      # Blog content strategy & editorial calendar
    seo-write-article/SKILL.md    # AI-assisted article writing (SEO + GEO)
    seo-outline-article/SKILL.md  # Article structure planning
    seo-wordpress-publish/SKILL.md # Publish to WordPress via REST API
    seo-brand-voice/SKILL.md      # Brand voice & editorial guidelines
    seo-cluster/                   # Semantic topic clustering
      SKILL.md
      references/
      templates/
    seo-content/SKILL.md          # E-E-A-T and content quality
    seo-page/SKILL.md             # Deep single-page analysis
    seo-schema/SKILL.md           # Schema.org markup
    seo-geo/SKILL.md              # AI search / GEO optimization
    seo-images/SKILL.md           # Image optimization
    seo-technical/SKILL.md        # Technical SEO
  agents/                            # 8 subagents
    seo-technical.md
    seo-content.md
    seo-schema.md
    seo-performance.md
    seo-visual.md
    seo-geo.md
    seo-wordpress.md
    seo-cluster.md
  hooks/
    hooks.json                     # PostToolUse schema validation
    validate-schema.py
  scripts/                           # 10 Python scripts
    wordpress_api.py               # WordPress REST API (read + write + publish)
    wp_content_analyzer.py         # Content deep analyzer (readability, clusters, E-E-A-T)
    georeadiness_analyzer.py       # GEO/AI citation readiness scorer
    llms_txt_generator.py          # llms.txt generator for WordPress
    fetch_page.py                  # Page fetcher with UA rotation
    parse_html.py                  # HTML parser for SEO elements
    pagespeed_check.py             # PageSpeed Insights v5 + CrUX API
    google_report.py               # PDF/HTML report generator
    capture_screenshot.py          # Playwright screenshots
    analyze_visual.py              # Visual analysis helper
  schema/                            # Schema.org JSON-LD templates
  docs/                              # Extended documentation
```

## Commands

| Command | Purpose |
|---------|---------|
| `/seo-audit <url>` | Full site audit with parallel subagents |
| `/seo-wordpress <url>` | WordPress blog SEO audit via REST API |
| `/seo-wp-strategy <url>` | Content strategy & editorial calendar |
| `/seo-write-article <keyword>` | AI-assisted article writing (SEO + GEO optimized) |
| `/seo-outline-article <keyword>` | Article structure planning (H1-H3, sources) |
| `/seo-wordpress-publish <file>` | Publish article to WordPress |
| `/seo-brand-voice` | Define/check brand voice & editorial guidelines |
| `/seo-cluster <seed-keyword>` | Topic clusters (pillar + secondary articles) |
| `/seo-content <url>` | E-E-A-T and content quality analysis |
| `/seo-page <url>` | Deep single-page analysis |
| `/seo-schema <url>` | Schema.org detection, validation, generation |
| `/seo-geo <url>` | AI search / GEO optimization |
| `/seo-images <url>` | Image optimization analysis |
| `/seo-technical <url>` | Technical SEO audit |

## Development Rules

- Keep SKILL.md files under 500 lines / 5000 tokens
- Reference files should be focused and under 200 lines
- Scripts must have docstrings, CLI interface, and JSON output
- Follow kebab-case naming for all skill directories
- Agents invoked via Agent tool, never via Bash
- Python dependencies install into `~/.claude/skills/seo/.venv/`

## Security Rules

- **Never commit credentials**: `.env`, `client_secret*.json`, `oauth-token.json` in `.gitignore`
- **URL validation**: All scripts call `validate_url()` for SSRF protection
- **No hardcoded paths**: Use `os.path.dirname(os.path.abspath(__file__))` for relative paths
- **Config location**: `~/.config/claude-seo/wordpress.json` (user-space, not in repo)

## Key Principles

1. **Blogger-First**: Every skill serves the blog content lifecycle (research → write → audit → publish)
2. **WordPress Native**: REST API integration with Application Password auth
3. **AI-Ready**: GEO optimization for ChatGPT, Perplexity, Google AI Overviews
4. **Pillar Strategy**: Topic clusters with hub-and-spoke architecture
