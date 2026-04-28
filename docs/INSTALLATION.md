# Installation Guide

**SEO Blogger Toolkit** by Abderrahim KHALID (MEDIA BUYING ACADEMY) - https://mediabuying.ac/
**Version:** 1.0.0

## Prerequisites

- **Python 3.10+** with pip
- **Git** for cloning the repository
- **Claude Code CLI** installed and configured

Optional:
- **Playwright** for screenshot capabilities

## Quick Install

### Unix/macOS/Linux

```bash
git clone https://github.com/Abderrahim-KHALID/claude-seo.git
cd claude-seo
./install.sh
```

### Windows (PowerShell)

```powershell
git clone --depth 1 https://github.com/Abderrahim-KHALID/claude-seo.git
cd claude-seo
powershell -ExecutionPolicy Bypass -File install.ps1
```

## Manual Installation

1. **Clone the repository**

```bash
git clone https://github.com/Abderrahim-KHALID/claude-seo.git
cd claude-seo
```

2. **Run the installer**

```bash
./install.sh
```

3. **Install Python dependencies** (if not done automatically)

The installer creates a venv at `~/.claude/skills/seo/.venv/`. If that fails, install manually:

```bash
# Option A: Use the venv
~/.claude/skills/seo/.venv/bin/pip install -r ~/.claude/skills/seo/requirements.txt

# Option B: User-level install
pip install --user -r ~/.claude/skills/seo/requirements.txt
```

4. **Install Playwright browsers** (optional, for visual analysis)

```bash
pip install playwright
playwright install chromium
```

Playwright is optional. Without it, visual analysis uses WebFetch as a fallback.

## Installation Paths

The installer copies files to:

| Component | Path |
|-----------|------|
| Main skill | `~/.claude/skills/seo/` |
| Sub-skills | `~/.claude/skills/seo-*/` |
| Subagents | `~/.claude/agents/seo-*.md` |

### What Gets Installed

**15 skills:**
- `seo` (main orchestrator)
- `seo-audit`, `seo-wordpress`, `seo-wp-strategy`
- `seo-write-article`, `seo-outline-article`, `seo-wordpress-publish`
- `seo-brand-voice`, `seo-cluster`, `seo-content`
- `seo-page`, `seo-schema`, `seo-geo`, `seo-images`, `seo-technical`

**8 agents:**
- `seo-technical`, `seo-content`, `seo-schema`, `seo-performance`
- `seo-visual`, `seo-geo`, `seo-wordpress`, `seo-cluster`

**10 scripts:**
- `wordpress_api.py`, `wp_content_analyzer.py`, `georeadiness_analyzer.py`
- `llms_txt_generator.py`, `fetch_page.py`, `parse_html.py`
- `pagespeed_check.py`, `google_report.py`, `capture_screenshot.py`, `analyze_visual.py`

## Verify Installation

1. Start Claude Code:

```bash
claude
```

2. Check that the skill is loaded:

```
/seo-audit
```

You should see a prompt asking for a URL to audit.

## Extensions (Optional)

Install optional extensions for additional capabilities:

```bash
# Banana Image Generation (Gemini AI)
./extensions/banana/install.sh

# DataForSEO live data
./extensions/dataforseo/install.sh

# Firecrawl web scraping
./extensions/firecrawl/install.sh
```

See [MCP-INTEGRATION.md](MCP-INTEGRATION.md) for details.

## Uninstallation

### Automatic

```bash
./uninstall.sh
```

### Manual

Remove all 15 skills:

```bash
rm -rf ~/.claude/skills/seo
rm -rf ~/.claude/skills/seo-audit
rm -rf ~/.claude/skills/seo-wordpress
rm -rf ~/.claude/skills/seo-wp-strategy
rm -rf ~/.claude/skills/seo-write-article
rm -rf ~/.claude/skills/seo-outline-article
rm -rf ~/.claude/skills/seo-wordpress-publish
rm -rf ~/.claude/skills/seo-brand-voice
rm -rf ~/.claude/skills/seo-cluster
rm -rf ~/.claude/skills/seo-content
rm -rf ~/.claude/skills/seo-page
rm -rf ~/.claude/skills/seo-schema
rm -rf ~/.claude/skills/seo-geo
rm -rf ~/.claude/skills/seo-images
rm -rf ~/.claude/skills/seo-technical
```

Remove all 8 agents:

```bash
rm -f ~/.claude/agents/seo-technical.md
rm -f ~/.claude/agents/seo-content.md
rm -f ~/.claude/agents/seo-schema.md
rm -f ~/.claude/agents/seo-performance.md
rm -f ~/.claude/agents/seo-visual.md
rm -f ~/.claude/agents/seo-geo.md
rm -f ~/.claude/agents/seo-wordpress.md
rm -f ~/.claude/agents/seo-cluster.md
```

Remove extensions (if installed):

```bash
# Banana
./extensions/banana/uninstall.sh

# DataForSEO
./extensions/dataforseo/uninstall.sh

# Firecrawl
./extensions/firecrawl/uninstall.sh
```

## Upgrading

To upgrade to the latest version:

```bash
cd claude-seo
git pull
./install.sh
```

## Troubleshooting

### "Skill not found" error

Ensure the skill is installed in the correct location:

```bash
ls ~/.claude/skills/seo/SKILL.md
```

If the file doesn't exist, re-run the installer.

### Python dependency errors

Install dependencies manually:

```bash
pip install beautifulsoup4 requests lxml playwright Pillow urllib3 validators
```

### Playwright screenshot errors

Install Chromium browser:

```bash
playwright install chromium
```

### Permission errors on Unix

Make sure scripts are executable:

```bash
chmod +x ~/.claude/skills/seo/scripts/*.py
```
