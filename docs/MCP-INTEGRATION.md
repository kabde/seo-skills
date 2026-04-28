# MCP Integration

**SEO Blogger Toolkit** by Abderrahim KHALID (MEDIA BUYING ACADEMY) - https://mediabuying.ac/

## Overview

SEO Blogger Toolkit can integrate with Model Context Protocol (MCP) servers to access external APIs and enhance analysis capabilities. Three bundled extensions are available, plus compatibility with third-party MCP servers.

## Bundled Extensions

### Banana Image Generation (Gemini AI)

AI image generation for SEO assets (OG images, hero images, product photos, infographics) powered by Gemini via nanobanana-mcp.

**Install:**
```bash
./extensions/banana/install.sh
```

**Uninstall:**
```bash
./extensions/banana/uninstall.sh
```

**What it adds:**
- `/seo-image-gen` skill with multiple use cases (OG, hero, product, infographic, custom, batch)
- `seo-image-gen` subagent for image auditing
- Creative Director pipeline with 6-component Reasoning Brief
- SEO checklist output (alt text, file naming, WebP, schema)

**Documentation:** See `extensions/banana/docs/BANANA-SETUP.md`

---

### DataForSEO

Live SEO data via DataForSEO MCP server. Provides SERP analysis, keyword research, backlink profiles, on-page analysis, content analysis, business listings, and AI visibility tracking.

**Install:**
```bash
./extensions/dataforseo/install.sh
```

**Uninstall:**
```bash
./extensions/dataforseo/uninstall.sh
```

**What it adds:**
- `/seo-dataforseo` skill with commands across multiple API modules
- `seo-dataforseo` subagent
- Field filtering configuration for API responses

**Documentation:** See `extensions/dataforseo/docs/DATAFORSEO-SETUP.md`

---

### Firecrawl

Advanced web scraping and crawling via Firecrawl MCP. Enables deep site analysis with JavaScript rendering support.

**Install:**
```bash
./extensions/firecrawl/install.sh
```

**Uninstall:**
```bash
./extensions/firecrawl/uninstall.sh
```

**What it adds:**
- `/seo-firecrawl` skill for advanced crawling
- JavaScript-rendered page fetching
- Structured data extraction at scale

**Documentation:** See `extensions/firecrawl/docs/FIRECRAWL-SETUP.md`

---

## Third-Party MCP Integrations

### PageSpeed Insights API

Use Google's PageSpeed Insights API directly for real Core Web Vitals data.

**Configuration:**

1. Get an API key from [Google Cloud Console](https://console.cloud.google.com/)
2. Enable the PageSpeed Insights API
3. Use in your analysis:

```bash
curl "https://www.googleapis.com/pagespeedonline/v5/runPagespeed?url=URL&key=YOUR_API_KEY"
```

### Google Search Console

For organic search data, use the `mcp-server-gsc` MCP server by [ahonn](https://github.com/ahonn/mcp-server-gsc). Provides search performance data, URL inspection, and sitemap management.

**Configuration:**

```json
{
  "mcpServers": {
    "google-search-console": {
      "command": "npx",
      "args": ["-y", "mcp-server-gsc"],
      "env": {
        "GOOGLE_CREDENTIALS_PATH": "/path/to/credentials.json"
      }
    }
  }
}
```

### PageSpeed Insights MCP Server

Use `mcp-server-pagespeed` by [enemyrr](https://github.com/enemyrr/mcp-server-pagespeed) for Lighthouse audits, CWV metrics, and performance scoring via MCP.

**Configuration:**

```json
{
  "mcpServers": {
    "pagespeed": {
      "command": "npx",
      "args": ["-y", "mcp-server-pagespeed"],
      "env": {
        "PAGESPEED_API_KEY": "your-api-key"
      }
    }
  }
}
```

### Other Compatible MCP Servers

| Tool | Package / Endpoint | Type | Notes |
|------|-------------------|------|-------|
| **Ahrefs** | `@ahrefs/mcp` | Official | Backlinks, keywords, site audit data |
| **Semrush** | `https://mcp.semrush.com/v1/mcp` | Official (remote) | Domain analytics, keyword research, backlink data |
| **Google Search Console** | `mcp-server-gsc` | Community | Search performance, URL inspection, sitemaps |
| **PageSpeed Insights** | `mcp-server-pagespeed` | Community | Lighthouse audits, CWV metrics, performance scoring |
| **kwrds.ai** | kwrds MCP server | Community | Keyword research, search volume, difficulty scoring |

## API Usage Examples

### PageSpeed Insights

```python
import requests

def get_pagespeed_data(url: str, api_key: str) -> dict:
    """Fetch PageSpeed Insights data for a URL."""
    endpoint = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
    params = {
        "url": url,
        "key": api_key,
        "strategy": "mobile",  # or "desktop"
        "category": ["performance", "accessibility", "best-practices", "seo"]
    }
    response = requests.get(endpoint, params=params)
    return response.json()
```

### Core Web Vitals from CrUX

```python
def get_crux_data(url: str, api_key: str) -> dict:
    """Fetch Chrome UX Report data for a URL."""
    endpoint = "https://chromeuxreport.googleapis.com/v1/records:queryRecord"
    payload = {
        "url": url,
        "formFactor": "PHONE"  # or "DESKTOP"
    }
    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}
    response = requests.post(endpoint, json=payload, headers=headers, params=params)
    return response.json()
```

## Metrics Available

### From PageSpeed Insights

| Metric | Description |
|--------|-------------|
| LCP | Largest Contentful Paint (lab) |
| INP | Interaction to Next Paint (estimated) |
| CLS | Cumulative Layout Shift (lab) |
| FCP | First Contentful Paint |
| TBT | Total Blocking Time |
| Speed Index | Visual progress speed |

### From CrUX (Field Data)

| Metric | Description |
|--------|-------------|
| LCP | 75th percentile, real users |
| INP | 75th percentile, real users |
| CLS | 75th percentile, real users |
| TTFB | Time to First Byte |

## Best Practices

1. **Rate Limiting**: Respect API quotas (typically 25k requests/day for PageSpeed)
2. **Caching**: Cache results to avoid redundant API calls
3. **Field vs Lab**: Prioritize field data (CrUX) for ranking signals
4. **Error Handling**: Handle API errors gracefully

## Without API Keys

If you don't have API keys or MCP extensions, SEO Blogger Toolkit can still:

1. Analyze HTML source for potential issues
2. Identify common performance problems
3. Check for render-blocking resources
4. Evaluate image optimization opportunities
5. Detect JavaScript-heavy implementations
6. Audit WordPress via REST API (no key needed for public endpoints)

The analysis will note that actual Core Web Vitals measurements require field data from real users.
