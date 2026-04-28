# Troubleshooting

**SEO Blogger Toolkit** by Abderrahim KHALID (MEDIA BUYING ACADEMY) - https://mediabuying.ac/

## Common Issues

### Skill Not Loading

**Symptom:** `/seo-audit` or other commands not recognized

**Solutions:**

1. Verify installation:
```bash
ls ~/.claude/skills/seo/SKILL.md
```

2. Check SKILL.md has proper frontmatter:
```bash
head -5 ~/.claude/skills/seo/SKILL.md
```
Should start with `---` followed by YAML.

3. Restart Claude Code:
```bash
claude
```

4. Re-run installer:
```bash
cd claude-seo
./install.sh
```

---

### Python Dependency Errors

**Symptom:** `ModuleNotFoundError: No module named 'requests'`

**Solution:**

Dependencies are installed in a venv. Try:

```bash
# Use the venv pip
~/.claude/skills/seo/.venv/bin/pip install -r ~/.claude/skills/seo/requirements.txt
```

If the venv doesn't exist, install with `--user`:
```bash
pip install --user -r ~/.claude/skills/seo/requirements.txt
```

Or install individually:
```bash
pip install --user beautifulsoup4 requests lxml playwright Pillow urllib3 validators
```

### requirements.txt Not Found

**Symptom:** `No such file: requirements.txt` after install

**Solution:** The file should be in the skill directory:

```bash
ls ~/.claude/skills/seo/requirements.txt
```

If missing, download it directly:
```bash
curl -fsSL https://raw.githubusercontent.com/Abderrahim-KHALID/claude-seo/main/requirements.txt \
  -o ~/.claude/skills/seo/requirements.txt
```

### Windows Python Detection Issues

**Symptom:** `python is not recognized` or `pip points to wrong Python`

**Solution:**

1. Install Python from [python.org](https://python.org) and check "Add to PATH"
2. Or use the Windows launcher: `py -3 -m pip install -r requirements.txt`
3. Use `python -m pip` instead of bare `pip`

---

### Playwright Screenshot Errors

**Symptom:** `playwright._impl._errors.Error: Executable doesn't exist`

**Solution:**
```bash
playwright install chromium
```

If that fails:
```bash
pip install playwright
python -m playwright install chromium
```

---

### Permission Denied Errors

**Symptom:** `Permission denied` when running scripts

**Solution:**
```bash
chmod +x ~/.claude/skills/seo/scripts/*.py
```

---

### Subagent Not Found

**Symptom:** `Agent 'seo-technical' not found` (or any of the 8 agents)

**Solution:**

1. Verify agent files exist:
```bash
ls ~/.claude/agents/seo-*.md
```

Expected agents: `seo-technical.md`, `seo-content.md`, `seo-schema.md`, `seo-performance.md`, `seo-visual.md`, `seo-geo.md`, `seo-wordpress.md`, `seo-cluster.md`

2. Check agent frontmatter:
```bash
head -5 ~/.claude/agents/seo-technical.md
```

3. Re-install agents:
```bash
cp /path/to/claude-seo/agents/*.md ~/.claude/agents/
```

---

### WordPress REST API Errors

**Symptom:** `/seo-wordpress` or `/seo-wordpress-publish` fails to connect

**Solutions:**

1. Verify the WordPress site has REST API enabled (most sites do by default)
2. Check the URL is correct and accessible
3. For publishing, ensure Application Password authentication is configured:
   - WordPress Admin > Users > Your Profile > Application Passwords
   - Store credentials in `~/.config/claude-seo/wordpress.json`
4. Some security plugins block REST API - check for `.htaccess` or plugin rules

---

### Timeout Errors

**Symptom:** `Request timed out after 30 seconds`

**Solutions:**

1. The target site may be slow: try again
2. Increase timeout in script calls
3. Check your network connection
4. Some sites block automated requests

---

### Schema Validation False Positives

**Symptom:** Hook blocks valid schema

**Check:**

1. Ensure placeholders are replaced
2. Verify @context is `https://schema.org`
3. Check for deprecated types (HowTo, SpecialAnnouncement)
4. Validate at [Google's Rich Results Test](https://search.google.com/test/rich-results)

---

### Slow Audit Performance

**Symptom:** `/seo-audit` takes too long

**Solutions:**

1. Large sites take time as the audit crawls multiple pages
2. All 8 subagents run in parallel to speed up analysis
3. For faster checks, use `/seo-page` on specific URLs
4. Check if site has slow response times

---

### Extension Issues

**Symptom:** Extension commands (`/seo-dataforseo`, `/seo-image-gen`, `/seo-firecrawl`) not working

**Solutions:**

1. Verify the extension is installed:
```bash
ls ~/.claude/skills/seo-dataforseo/SKILL.md
ls ~/.claude/skills/seo-image-gen/SKILL.md
ls ~/.claude/skills/seo-firecrawl/SKILL.md
```

2. Re-run the extension installer:
```bash
./extensions/dataforseo/install.sh
./extensions/banana/install.sh
./extensions/firecrawl/install.sh
```

3. Check MCP server configuration in `~/.claude/settings.json`

---

## Getting Help

1. **Check the docs:** Review [COMMANDS.md](COMMANDS.md) and [ARCHITECTURE.md](ARCHITECTURE.md)

2. **GitHub Issues:** Report bugs at the repository

3. **Website:** https://mediabuying.ac/

4. **Logs:** Check Claude Code's output for error details

## Debug Mode

To see detailed output, run scripts directly:

```bash
# Test fetch
python3 ~/.claude/skills/seo/scripts/fetch_page.py https://example.com

# Test parse
python3 ~/.claude/skills/seo/scripts/parse_html.py page.html --json

# Test screenshot
python3 ~/.claude/skills/seo/scripts/capture_screenshot.py https://example.com

# Test WordPress API
python3 ~/.claude/skills/seo/scripts/wordpress_api.py https://myblog.com

# Test GEO readiness
python3 ~/.claude/skills/seo/scripts/georeadiness_analyzer.py https://example.com/article
```
